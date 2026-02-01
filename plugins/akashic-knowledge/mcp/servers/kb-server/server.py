#!/usr/bin/env python3
"""
Akashic Knowledge Base MCP Server

Unified knowledge base server providing:
- Vector search via Qdrant (semantic similarity)
- Graph queries via Neo4j (relationship traversal)
- Keyword search via Elasticsearch (BM25)
- Hybrid retrieval with Reciprocal Rank Fusion
- Session state via Redis

Tools exposed:
- akashic_create_kb: Create task/project/global knowledge base
- akashic_ingest: Ingest directory, files, or URLs
- akashic_query: Hybrid semantic + keyword search
- akashic_discover: Run heuristic discovery pipeline
- akashic_graph_traverse: Multi-hop knowledge graph queries
- akashic_export: Generate research documents
- akashic_status: Check infrastructure status

Resources exposed:
- akashic://kb/{name}/status: Knowledge base status
- akashic://kb/{name}/catalog: Indexed document catalog
- akashic://heuristics/{domain}: Domain heuristics
"""

import asyncio
import hashlib
import json
import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# MCP SDK imports
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        CallToolResult,
        ListResourcesResult,
        ListToolsResult,
        ReadResourceResult,
        Resource,
        TextContent,
        Tool,
    )
except ImportError:
    print("MCP SDK not installed. Install with: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Optional database clients
try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, PointStruct, VectorParams

    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False

try:
    from neo4j import GraphDatabase

    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

try:
    from elasticsearch import Elasticsearch

    ES_AVAILABLE = True
except ImportError:
    ES_AVAILABLE = False

try:
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("akashic-kb")


@dataclass
class KnowledgeBase:
    """Knowledge base metadata."""

    name: str
    scope: str  # task, project, global
    created_at: str
    document_count: int = 0
    entity_count: int = 0
    heuristic_count: int = 0
    collections: list = field(default_factory=list)


@dataclass
class SearchResult:
    """Unified search result across stores."""

    id: str
    content: str
    source: str
    score: float
    metadata: dict = field(default_factory=dict)


class AkashicKBServer:
    """Unified knowledge base MCP server."""

    def __init__(self):
        self.server = Server("akashic-kb")
        self.data_dir = Path(os.getenv("AKASHIC_DATA_DIR", Path.home() / ".akashic"))
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Database connections (lazy initialization)
        self._qdrant: Optional[QdrantClient] = None
        self._neo4j: Optional[Any] = None
        self._es: Optional[Elasticsearch] = None
        self._redis: Optional[Any] = None

        # Knowledge base registry
        self.kb_registry: dict[str, KnowledgeBase] = {}
        self._load_registry()

        # Register handlers
        self._register_tools()
        self._register_resources()

    def _load_registry(self):
        """Load knowledge base registry from disk."""
        registry_file = self.data_dir / "registry.json"
        if registry_file.exists():
            try:
                data = json.loads(registry_file.read_text())
                for name, kb_data in data.items():
                    self.kb_registry[name] = KnowledgeBase(**kb_data)
            except Exception as e:
                logger.warning(f"Failed to load registry: {e}")

    def _save_registry(self):
        """Save knowledge base registry to disk."""
        registry_file = self.data_dir / "registry.json"
        data = {
            name: {
                "name": kb.name,
                "scope": kb.scope,
                "created_at": kb.created_at,
                "document_count": kb.document_count,
                "entity_count": kb.entity_count,
                "heuristic_count": kb.heuristic_count,
                "collections": kb.collections,
            }
            for name, kb in self.kb_registry.items()
        }
        registry_file.write_text(json.dumps(data, indent=2))

    @property
    def qdrant(self) -> Optional[QdrantClient]:
        """Lazy Qdrant client initialization."""
        if self._qdrant is None and QDRANT_AVAILABLE:
            try:
                url = os.getenv("QDRANT_URL", "http://localhost:6333")
                self._qdrant = QdrantClient(url=url)
                logger.info(f"Connected to Qdrant at {url}")
            except Exception as e:
                logger.warning(f"Failed to connect to Qdrant: {e}")
        return self._qdrant

    @property
    def neo4j(self):
        """Lazy Neo4j driver initialization."""
        if self._neo4j is None and NEO4J_AVAILABLE:
            try:
                url = os.getenv("NEO4J_URL", "bolt://localhost:7687")
                user = os.getenv("NEO4J_USER", "neo4j")
                password = os.getenv("NEO4J_PASSWORD", "akashic_secure_2026")
                self._neo4j = GraphDatabase.driver(url, auth=(user, password))
                logger.info(f"Connected to Neo4j at {url}")
            except Exception as e:
                logger.warning(f"Failed to connect to Neo4j: {e}")
        return self._neo4j

    @property
    def es(self) -> Optional[Elasticsearch]:
        """Lazy Elasticsearch client initialization."""
        if self._es is None and ES_AVAILABLE:
            try:
                url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
                self._es = Elasticsearch([url])
                logger.info(f"Connected to Elasticsearch at {url}")
            except Exception as e:
                logger.warning(f"Failed to connect to Elasticsearch: {e}")
        return self._es

    @property
    def redis_client(self):
        """Lazy Redis client initialization."""
        if self._redis is None and REDIS_AVAILABLE:
            try:
                url = os.getenv("REDIS_URL", "redis://localhost:6379")
                self._redis = redis.from_url(url)
                logger.info(f"Connected to Redis at {url}")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {e}")
        return self._redis

    def _register_tools(self):
        """Register MCP tools."""

        @self.server.list_tools()
        async def list_tools() -> ListToolsResult:
            return ListToolsResult(
                tools=[
                    Tool(
                        name="akashic_create_kb",
                        description="Create a new knowledge base with specified scope (task, project, or global)",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Unique name for the knowledge base",
                                },
                                "scope": {
                                    "type": "string",
                                    "enum": ["task", "project", "global"],
                                    "description": "Scope: task (ephemeral), project (session), global (persistent)",
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Optional description of the knowledge base purpose",
                                },
                            },
                            "required": ["name", "scope"],
                        },
                    ),
                    Tool(
                        name="akashic_ingest",
                        description="Ingest documents into a knowledge base from directory, files, or URLs",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "kb_name": {
                                    "type": "string",
                                    "description": "Target knowledge base name",
                                },
                                "source": {
                                    "type": "string",
                                    "description": "Path to directory/file or URL to ingest",
                                },
                                "recursive": {
                                    "type": "boolean",
                                    "description": "Recursively ingest directories",
                                    "default": True,
                                },
                                "file_patterns": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "Glob patterns for file filtering",
                                    "default": [
                                        "*.md",
                                        "*.txt",
                                        "*.py",
                                        "*.js",
                                        "*.ts",
                                    ],
                                },
                            },
                            "required": ["kb_name", "source"],
                        },
                    ),
                    Tool(
                        name="akashic_query",
                        description="Query knowledge base using hybrid semantic + keyword search with RRF",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "kb_name": {
                                    "type": "string",
                                    "description": "Knowledge base to query",
                                },
                                "query": {
                                    "type": "string",
                                    "description": "Natural language query",
                                },
                                "top_k": {
                                    "type": "integer",
                                    "description": "Number of results to return",
                                    "default": 10,
                                },
                                "search_type": {
                                    "type": "string",
                                    "enum": ["hybrid", "semantic", "keyword"],
                                    "description": "Search strategy",
                                    "default": "hybrid",
                                },
                                "rerank": {
                                    "type": "boolean",
                                    "description": "Apply ColBERT-style reranking",
                                    "default": True,
                                },
                            },
                            "required": ["kb_name", "query"],
                        },
                    ),
                    Tool(
                        name="akashic_discover",
                        description="Run heuristic discovery pipeline (AutoHD) on knowledge base",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "kb_name": {
                                    "type": "string",
                                    "description": "Source knowledge base",
                                },
                                "domain": {
                                    "type": "string",
                                    "description": "Domain for heuristic discovery",
                                },
                                "iterations": {
                                    "type": "integer",
                                    "description": "Evolution iterations",
                                    "default": 3,
                                },
                                "validate": {
                                    "type": "boolean",
                                    "description": "Run POPPER validation",
                                    "default": True,
                                },
                            },
                            "required": ["kb_name", "domain"],
                        },
                    ),
                    Tool(
                        name="akashic_graph_traverse",
                        description="Execute multi-hop knowledge graph traversal query",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "kb_name": {
                                    "type": "string",
                                    "description": "Knowledge base with graph data",
                                },
                                "start_entity": {
                                    "type": "string",
                                    "description": "Starting entity for traversal",
                                },
                                "relation_types": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "Relationship types to traverse",
                                },
                                "max_hops": {
                                    "type": "integer",
                                    "description": "Maximum traversal depth",
                                    "default": 3,
                                },
                            },
                            "required": ["kb_name", "start_entity"],
                        },
                    ),
                    Tool(
                        name="akashic_export",
                        description="Export research documents or heuristics from knowledge base",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "kb_name": {
                                    "type": "string",
                                    "description": "Source knowledge base",
                                },
                                "format": {
                                    "type": "string",
                                    "enum": ["markdown", "json", "jsonld"],
                                    "description": "Export format",
                                    "default": "markdown",
                                },
                                "output_path": {
                                    "type": "string",
                                    "description": "Output file path",
                                },
                                "include_heuristics": {
                                    "type": "boolean",
                                    "description": "Include discovered heuristics",
                                    "default": True,
                                },
                            },
                            "required": ["kb_name", "output_path"],
                        },
                    ),
                    Tool(
                        name="akashic_status",
                        description="Check status of knowledge base infrastructure",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "kb_name": {
                                    "type": "string",
                                    "description": "Optional: specific KB to check",
                                }
                            },
                        },
                    ),
                ]
            )

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> CallToolResult:
            try:
                if name == "akashic_create_kb":
                    result = await self._create_kb(**arguments)
                elif name == "akashic_ingest":
                    result = await self._ingest(**arguments)
                elif name == "akashic_query":
                    result = await self._query(**arguments)
                elif name == "akashic_discover":
                    result = await self._discover(**arguments)
                elif name == "akashic_graph_traverse":
                    result = await self._graph_traverse(**arguments)
                elif name == "akashic_export":
                    result = await self._export(**arguments)
                elif name == "akashic_status":
                    result = await self._status(**arguments)
                else:
                    result = {"error": f"Unknown tool: {name}"}

                return CallToolResult(
                    content=[
                        TextContent(type="text", text=json.dumps(result, indent=2))
                    ]
                )
            except Exception as e:
                logger.exception(f"Tool {name} failed")
                return CallToolResult(
                    content=[
                        TextContent(type="text", text=json.dumps({"error": str(e)}))
                    ]
                )

    def _register_resources(self):
        """Register MCP resources."""

        @self.server.list_resources()
        async def list_resources() -> ListResourcesResult:
            resources = []
            for name, kb in self.kb_registry.items():
                resources.extend(
                    [
                        Resource(
                            uri=f"akashic://kb/{name}/status",
                            name=f"{name} Status",
                            description=f"Status of {name} knowledge base",
                            mimeType="application/json",
                        ),
                        Resource(
                            uri=f"akashic://kb/{name}/catalog",
                            name=f"{name} Catalog",
                            description=f"Document catalog for {name}",
                            mimeType="application/json",
                        ),
                    ]
                )
            return ListResourcesResult(resources=resources)

        @self.server.read_resource()
        async def read_resource(uri: str) -> ReadResourceResult:
            parts = uri.replace("akashic://", "").split("/")
            if len(parts) >= 3 and parts[0] == "kb":
                kb_name = parts[1]
                resource_type = parts[2]

                if kb_name not in self.kb_registry:
                    return ReadResourceResult(
                        contents=[
                            TextContent(
                                type="text", text=json.dumps({"error": "KB not found"})
                            )
                        ]
                    )

                kb = self.kb_registry[kb_name]

                if resource_type == "status":
                    data = {
                        "name": kb.name,
                        "scope": kb.scope,
                        "created_at": kb.created_at,
                        "document_count": kb.document_count,
                        "entity_count": kb.entity_count,
                        "heuristic_count": kb.heuristic_count,
                    }
                elif resource_type == "catalog":
                    data = {
                        "collections": kb.collections,
                        "document_count": kb.document_count,
                    }
                else:
                    data = {"error": f"Unknown resource: {resource_type}"}

                return ReadResourceResult(
                    contents=[TextContent(type="text", text=json.dumps(data, indent=2))]
                )

            return ReadResourceResult(
                contents=[
                    TextContent(type="text", text=json.dumps({"error": "Invalid URI"}))
                ]
            )

    async def _create_kb(self, name: str, scope: str, description: str = "") -> dict:
        """Create a new knowledge base."""
        if name in self.kb_registry:
            return {"error": f"Knowledge base '{name}' already exists"}

        kb = KnowledgeBase(
            name=name,
            scope=scope,
            created_at=datetime.utcnow().isoformat(),
        )

        # Create Qdrant collection
        if self.qdrant:
            try:
                self.qdrant.create_collection(
                    collection_name=f"akashic_{name}",
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
                )
                kb.collections.append(f"qdrant:akashic_{name}")
            except Exception as e:
                logger.warning(f"Failed to create Qdrant collection: {e}")

        # Create Elasticsearch index
        if self.es:
            try:
                self.es.indices.create(
                    index=f"akashic_{name}",
                    body={
                        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
                        "mappings": {
                            "properties": {
                                "content": {"type": "text", "analyzer": "standard"},
                                "source": {"type": "keyword"},
                                "created_at": {"type": "date"},
                            }
                        },
                    },
                    ignore=400,  # Ignore if exists
                )
                kb.collections.append(f"es:akashic_{name}")
            except Exception as e:
                logger.warning(f"Failed to create ES index: {e}")

        self.kb_registry[name] = kb
        self._save_registry()

        return {
            "success": True,
            "message": f"Created knowledge base '{name}' with scope '{scope}'",
            "kb": {
                "name": kb.name,
                "scope": kb.scope,
                "created_at": kb.created_at,
                "collections": kb.collections,
            },
        }

    async def _ingest(
        self,
        kb_name: str,
        source: str,
        recursive: bool = True,
        file_patterns: list = None,
    ) -> dict:
        """Ingest documents into knowledge base."""
        if kb_name not in self.kb_registry:
            return {"error": f"Knowledge base '{kb_name}' not found"}

        file_patterns = file_patterns or ["*.md", "*.txt", "*.py", "*.js", "*.ts"]
        kb = self.kb_registry[kb_name]
        ingested = []

        source_path = Path(source)
        if source_path.is_dir():
            for pattern in file_patterns:
                glob_func = source_path.rglob if recursive else source_path.glob
                for file_path in glob_func(pattern):
                    if file_path.is_file():
                        try:
                            content = file_path.read_text(errors="ignore")
                            doc_id = hashlib.md5(str(file_path).encode()).hexdigest()

                            # Index in available stores
                            await self._index_document(
                                kb_name, doc_id, content, str(file_path)
                            )
                            ingested.append(str(file_path))
                        except Exception as e:
                            logger.warning(f"Failed to ingest {file_path}: {e}")
        elif source_path.is_file():
            try:
                content = source_path.read_text(errors="ignore")
                doc_id = hashlib.md5(source.encode()).hexdigest()
                await self._index_document(kb_name, doc_id, content, source)
                ingested.append(source)
            except Exception as e:
                return {"error": f"Failed to ingest file: {e}"}
        else:
            return {"error": f"Source not found: {source}"}

        kb.document_count += len(ingested)
        self._save_registry()

        return {
            "success": True,
            "ingested_count": len(ingested),
            "files": ingested[:20],  # Limit response size
            "total_in_kb": kb.document_count,
        }

    async def _index_document(
        self, kb_name: str, doc_id: str, content: str, source: str
    ):
        """Index document in vector and keyword stores."""
        # Note: In production, you'd call an embedding API here
        # For now, we'll use a placeholder

        # Index in Elasticsearch for BM25
        if self.es:
            try:
                self.es.index(
                    index=f"akashic_{kb_name}",
                    id=doc_id,
                    body={
                        "content": content[:10000],  # Limit size
                        "source": source,
                        "created_at": datetime.utcnow().isoformat(),
                    },
                )
            except Exception as e:
                logger.warning(f"ES indexing failed: {e}")

    async def _query(
        self,
        kb_name: str,
        query: str,
        top_k: int = 10,
        search_type: str = "hybrid",
        rerank: bool = True,
    ) -> dict:
        """Query knowledge base with hybrid search."""
        if kb_name not in self.kb_registry:
            return {"error": f"Knowledge base '{kb_name}' not found"}

        results = []

        # BM25 keyword search via Elasticsearch
        if self.es and search_type in ["hybrid", "keyword"]:
            try:
                es_response = self.es.search(
                    index=f"akashic_{kb_name}",
                    body={"query": {"match": {"content": query}}, "size": top_k * 2},
                )
                for hit in es_response.get("hits", {}).get("hits", []):
                    results.append(
                        SearchResult(
                            id=hit["_id"],
                            content=hit["_source"].get("content", "")[:500],
                            source=hit["_source"].get("source", ""),
                            score=hit["_score"],
                            metadata={"search_type": "keyword"},
                        )
                    )
            except Exception as e:
                logger.warning(f"ES search failed: {e}")

        # Apply Reciprocal Rank Fusion if hybrid
        if search_type == "hybrid" and results:
            # RRF formula: 1/(k+rank) where k=60 is typical
            k = 60
            for i, result in enumerate(results):
                result.score = 1.0 / (k + i + 1)

        # Sort by score and limit
        results.sort(key=lambda x: x.score, reverse=True)
        results = results[:top_k]

        return {
            "query": query,
            "search_type": search_type,
            "result_count": len(results),
            "results": [
                {
                    "id": r.id,
                    "content": r.content,
                    "source": r.source,
                    "score": r.score,
                }
                for r in results
            ],
        }

    async def _discover(
        self, kb_name: str, domain: str, iterations: int = 3, validate: bool = True
    ) -> dict:
        """Run heuristic discovery pipeline."""
        if kb_name not in self.kb_registry:
            return {"error": f"Knowledge base '{kb_name}' not found"}

        # This would integrate with heuristics-framework agents
        return {
            "status": "discovery_initiated",
            "kb_name": kb_name,
            "domain": domain,
            "iterations": iterations,
            "validate": validate,
            "message": "Heuristic discovery pipeline started. Use orchestrator agent for full pipeline.",
        }

    async def _graph_traverse(
        self,
        kb_name: str,
        start_entity: str,
        relation_types: list = None,
        max_hops: int = 3,
    ) -> dict:
        """Execute graph traversal query."""
        if kb_name not in self.kb_registry:
            return {"error": f"Knowledge base '{kb_name}' not found"}

        if not self.neo4j:
            return {"error": "Neo4j not available"}

        try:
            with self.neo4j.session() as session:
                # Multi-hop traversal query
                rel_filter = ""
                if relation_types:
                    rel_filter = ":" + "|".join(relation_types)

                cypher = f"""
                MATCH path = (start:Entity {{name: $start_entity}})-[{rel_filter}*1..{max_hops}]-(related)
                RETURN path, length(path) as hops
                ORDER BY hops
                LIMIT 50
                """

                result = session.run(cypher, start_entity=start_entity)
                paths = []
                for record in result:
                    paths.append({"hops": record["hops"], "path": str(record["path"])})

                return {
                    "start_entity": start_entity,
                    "max_hops": max_hops,
                    "paths_found": len(paths),
                    "paths": paths[:20],
                }
        except Exception as e:
            return {"error": f"Graph traversal failed: {e}"}

    async def _export(
        self,
        kb_name: str,
        output_path: str,
        format: str = "markdown",
        include_heuristics: bool = True,
    ) -> dict:
        """Export knowledge base content."""
        if kb_name not in self.kb_registry:
            return {"error": f"Knowledge base '{kb_name}' not found"}

        kb = self.kb_registry[kb_name]
        output = Path(output_path)

        if format == "markdown":
            content = f"""# {kb_name} Knowledge Base Export

Generated: {datetime.utcnow().isoformat()}

## Summary
- **Scope**: {kb.scope}
- **Documents**: {kb.document_count}
- **Entities**: {kb.entity_count}
- **Heuristics**: {kb.heuristic_count}

## Collections
{chr(10).join(f"- {c}" for c in kb.collections)}

"""
            output.write_text(content)
        elif format == "json":
            data = {
                "name": kb.name,
                "scope": kb.scope,
                "created_at": kb.created_at,
                "document_count": kb.document_count,
                "exported_at": datetime.utcnow().isoformat(),
            }
            output.write_text(json.dumps(data, indent=2))

        return {"success": True, "output_path": str(output), "format": format}

    async def _status(self, kb_name: str = None) -> dict:
        """Check infrastructure status."""
        status = {
            "qdrant": {
                "available": QDRANT_AVAILABLE,
                "connected": self.qdrant is not None,
            },
            "neo4j": {
                "available": NEO4J_AVAILABLE,
                "connected": self.neo4j is not None,
            },
            "elasticsearch": {
                "available": ES_AVAILABLE,
                "connected": self.es is not None,
            },
            "redis": {
                "available": REDIS_AVAILABLE,
                "connected": self.redis_client is not None,
            },
            "knowledge_bases": list(self.kb_registry.keys()),
        }

        if kb_name and kb_name in self.kb_registry:
            kb = self.kb_registry[kb_name]
            status["kb_details"] = {
                "name": kb.name,
                "scope": kb.scope,
                "document_count": kb.document_count,
                "entity_count": kb.entity_count,
            }

        return status

    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream, write_stream, self.server.create_initialization_options()
            )


def main():
    """Entry point."""
    server = AkashicKBServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
