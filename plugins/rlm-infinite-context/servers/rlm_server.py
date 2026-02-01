#!/usr/bin/env python3
"""
RLM (Recursive Language Model) MCP Server

Implements MIT's Recursive Language Model technique for processing arbitrarily
long contexts by storing content externally and providing recursive search tools.

Key insight: Long prompts should not be fed into the neural network directly.
Instead, they should be treated as part of the environment that the LLM can
symbolically interact with.
"""

import asyncio
import json
import logging
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from collections import defaultdict
import hashlib

# Configure logging to stderr (MCP requirement)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr
)
logger = logging.getLogger("rlm-server")


@dataclass
class ContextStore:
    """Manages stored contexts for RLM processing."""
    id: str
    name: str
    content: str
    token_estimate: int
    created_at: str
    metadata: dict = field(default_factory=dict)
    chunks: list = field(default_factory=list)
    

@dataclass
class SearchResult:
    """A single search result with context."""
    chunk_id: int
    content: str
    start_char: int
    end_char: int
    relevance_score: float
    match_count: int
    context_before: str = ""
    context_after: str = ""
    

@dataclass
class RecursiveQuery:
    """Tracks a recursive query and its sub-queries."""
    query_id: str
    parent_id: Optional[str]
    depth: int
    query: str
    context_id: str
    results: list = field(default_factory=list)
    sub_queries: list = field(default_factory=list)
    tokens_used: int = 0
    timestamp: str = ""


class RLMServer:
    """
    RLM MCP Server implementation.
    
    Provides tools for:
    - Loading large contexts into external storage
    - Searching through contexts with various strategies
    - Recursive sub-querying for deep information retrieval
    - Cost and token tracking
    """
    
    def __init__(self):
        self.data_dir = Path(os.environ.get("RLM_DATA_DIR", "./data"))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.max_depth = int(os.environ.get("RLM_MAX_DEPTH", "10"))
        self.chunk_size = int(os.environ.get("RLM_CHUNK_SIZE", "4000"))
        self.overlap = int(os.environ.get("RLM_OVERLAP", "200"))
        
        # In-memory stores
        self.contexts: dict[str, ContextStore] = {}
        self.queries: dict[str, RecursiveQuery] = {}
        self.active_session: Optional[str] = None
        
        # Statistics tracking
        self.stats = {
            "total_queries": 0,
            "total_tokens_processed": 0,
            "max_depth_reached": 0,
            "contexts_loaded": 0
        }
        
        logger.info(f"RLM Server initialized. Data dir: {self.data_dir}")
        
    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation (4 chars per token average)."""
        return len(text) // 4
    
    def generate_id(self, content: str) -> str:
        """Generate a unique ID for content."""
        return hashlib.sha256(content[:1000].encode()).hexdigest()[:12]
    
    def chunk_content(self, content: str) -> list[dict]:
        """
        Split content into overlapping chunks for efficient searching.
        Uses semantic boundaries when possible.
        """
        chunks = []
        lines = content.split('\n')
        current_chunk = []
        current_size = 0
        chunk_start = 0
        char_position = 0
        
        for i, line in enumerate(lines):
            line_size = len(line) + 1  # +1 for newline
            
            # Check if adding this line exceeds chunk size
            if current_size + line_size > self.chunk_size and current_chunk:
                chunk_text = '\n'.join(current_chunk)
                chunks.append({
                    "id": len(chunks),
                    "content": chunk_text,
                    "start_char": chunk_start,
                    "end_char": char_position,
                    "start_line": chunk_start,
                    "tokens": self.estimate_tokens(chunk_text)
                })
                
                # Keep overlap
                overlap_lines = []
                overlap_size = 0
                for prev_line in reversed(current_chunk):
                    if overlap_size + len(prev_line) < self.overlap:
                        overlap_lines.insert(0, prev_line)
                        overlap_size += len(prev_line) + 1
                    else:
                        break
                
                current_chunk = overlap_lines
                current_size = overlap_size
                chunk_start = char_position - overlap_size
            
            current_chunk.append(line)
            current_size += line_size
            char_position += line_size
        
        # Add final chunk
        if current_chunk:
            chunk_text = '\n'.join(current_chunk)
            chunks.append({
                "id": len(chunks),
                "content": chunk_text,
                "start_char": chunk_start,
                "end_char": char_position,
                "start_line": chunk_start,
                "tokens": self.estimate_tokens(chunk_text)
            })
        
        return chunks
    
    def search_regex(self, context: ContextStore, pattern: str, 
                     flags: int = re.IGNORECASE) -> list[SearchResult]:
        """Search using regex pattern."""
        results = []
        try:
            compiled = re.compile(pattern, flags)
            
            for chunk in context.chunks:
                matches = list(compiled.finditer(chunk["content"]))
                if matches:
                    # Calculate relevance based on match density
                    relevance = len(matches) / (len(chunk["content"]) / 100)
                    results.append(SearchResult(
                        chunk_id=chunk["id"],
                        content=chunk["content"],
                        start_char=chunk["start_char"],
                        end_char=chunk["end_char"],
                        relevance_score=min(relevance, 1.0),
                        match_count=len(matches)
                    ))
        except re.error as e:
            logger.error(f"Regex error: {e}")
            
        return sorted(results, key=lambda x: x.relevance_score, reverse=True)
    
    def search_keyword(self, context: ContextStore, keywords: list[str],
                       match_all: bool = False) -> list[SearchResult]:
        """Search for keywords in context."""
        results = []
        
        for chunk in context.chunks:
            content_lower = chunk["content"].lower()
            matches = sum(1 for kw in keywords if kw.lower() in content_lower)
            
            if match_all and matches < len(keywords):
                continue
            if matches == 0:
                continue
                
            relevance = matches / len(keywords)
            results.append(SearchResult(
                chunk_id=chunk["id"],
                content=chunk["content"],
                start_char=chunk["start_char"],
                end_char=chunk["end_char"],
                relevance_score=relevance,
                match_count=matches
            ))
        
        return sorted(results, key=lambda x: x.relevance_score, reverse=True)
    
    def search_semantic_sections(self, context: ContextStore, 
                                 section_pattern: str) -> list[SearchResult]:
        """
        Search for semantic sections (chapters, functions, etc.)
        Uses heuristics to identify logical document sections.
        """
        results = []
        
        # Common section patterns
        patterns = [
            r'^#{1,6}\s+' + section_pattern,  # Markdown headers
            r'^(Chapter|Section|Part)\s+\d*:?\s*' + section_pattern,  # Book sections
            r'^(def|class|function)\s+' + section_pattern,  # Code definitions
            r'^<' + section_pattern + r'[^>]*>',  # XML/HTML tags
            r'^\d+\.\d*\s+' + section_pattern,  # Numbered sections
        ]
        
        combined_pattern = '|'.join(f'({p})' for p in patterns)
        
        try:
            compiled = re.compile(combined_pattern, re.MULTILINE | re.IGNORECASE)
            
            for chunk in context.chunks:
                matches = list(compiled.finditer(chunk["content"]))
                if matches:
                    results.append(SearchResult(
                        chunk_id=chunk["id"],
                        content=chunk["content"],
                        start_char=chunk["start_char"],
                        end_char=chunk["end_char"],
                        relevance_score=len(matches) / 10,
                        match_count=len(matches)
                    ))
        except re.error:
            pass
            
        return sorted(results, key=lambda x: x.relevance_score, reverse=True)
    
    def get_context_window(self, context: ContextStore, chunk_id: int,
                           window_size: int = 1) -> str:
        """Get a chunk with surrounding context."""
        start_idx = max(0, chunk_id - window_size)
        end_idx = min(len(context.chunks), chunk_id + window_size + 1)
        
        chunks = context.chunks[start_idx:end_idx]
        return '\n'.join(c["content"] for c in chunks)
    
    # === MCP Tool Implementations ===
    
    async def load_context(self, content: str, name: str = "default",
                          metadata: dict = None) -> dict:
        """
        Load a large context into RLM storage.
        
        The context is chunked and indexed for efficient recursive searching.
        This is the first step in the RLM workflow.
        """
        context_id = self.generate_id(content)
        
        # Chunk the content
        chunks = self.chunk_content(content)
        
        context = ContextStore(
            id=context_id,
            name=name,
            content=content,
            token_estimate=self.estimate_tokens(content),
            created_at=datetime.now().isoformat(),
            metadata=metadata or {},
            chunks=chunks
        )
        
        self.contexts[context_id] = context
        self.active_session = context_id
        self.stats["contexts_loaded"] += 1
        
        # Save to disk for persistence
        context_file = self.data_dir / f"{context_id}.json"
        with open(context_file, 'w') as f:
            json.dump({
                "id": context_id,
                "name": name,
                "token_estimate": context.token_estimate,
                "chunk_count": len(chunks),
                "created_at": context.created_at,
                "metadata": metadata or {}
            }, f, indent=2)
        
        # Save content separately (large file)
        content_file = self.data_dir / f"{context_id}.txt"
        with open(content_file, 'w') as f:
            f.write(content)
        
        return {
            "success": True,
            "context_id": context_id,
            "name": name,
            "token_estimate": context.token_estimate,
            "chunk_count": len(chunks),
            "message": f"Context loaded successfully. Use search tools to query {context.token_estimate:,} tokens across {len(chunks)} chunks."
        }
    
    async def search_context(self, query: str, context_id: str = None,
                            search_type: str = "auto", top_k: int = 5,
                            parent_query_id: str = None) -> dict:
        """
        Search through a loaded context.
        
        Search types:
        - auto: Automatically determine best search strategy
        - regex: Use regex pattern matching
        - keyword: Search for keywords
        - section: Find semantic sections (chapters, functions, etc.)
        
        This is the core RLM search operation.
        """
        context_id = context_id or self.active_session
        if not context_id or context_id not in self.contexts:
            return {"error": "No context loaded. Use rlm_load first."}
        
        context = self.contexts[context_id]
        
        # Determine search depth
        depth = 0
        if parent_query_id and parent_query_id in self.queries:
            depth = self.queries[parent_query_id].depth + 1
            if depth > self.max_depth:
                return {
                    "error": f"Maximum recursion depth ({self.max_depth}) reached.",
                    "suggestion": "Try a different search strategy or broaden your query."
                }
        
        # Create query record
        query_id = f"q_{len(self.queries)}_{self.generate_id(query)[:6]}"
        query_record = RecursiveQuery(
            query_id=query_id,
            parent_id=parent_query_id,
            depth=depth,
            query=query,
            context_id=context_id,
            timestamp=datetime.now().isoformat()
        )
        
        # Auto-detect search type
        if search_type == "auto":
            if re.search(r'[*+?\\.\[\]{}()^$|]', query):
                search_type = "regex"
            elif any(kw in query.lower() for kw in ['chapter', 'section', 'function', 'class', 'def']):
                search_type = "section"
            else:
                search_type = "keyword"
        
        # Execute search
        if search_type == "regex":
            results = self.search_regex(context, query)
        elif search_type == "section":
            results = self.search_semantic_sections(context, query)
        else:
            keywords = [kw.strip() for kw in query.split() if len(kw.strip()) > 2]
            results = self.search_keyword(context, keywords)
        
        # Limit results
        results = results[:top_k]
        
        # Calculate tokens used
        tokens_used = sum(self.estimate_tokens(r.content) for r in results)
        query_record.tokens_used = tokens_used
        query_record.results = [asdict(r) for r in results]
        
        # Store query
        self.queries[query_id] = query_record
        self.stats["total_queries"] += 1
        self.stats["total_tokens_processed"] += tokens_used
        self.stats["max_depth_reached"] = max(self.stats["max_depth_reached"], depth)
        
        # Link to parent
        if parent_query_id and parent_query_id in self.queries:
            self.queries[parent_query_id].sub_queries.append(query_id)
        
        return {
            "query_id": query_id,
            "search_type": search_type,
            "depth": depth,
            "result_count": len(results),
            "tokens_returned": tokens_used,
            "results": [
                {
                    "chunk_id": r.chunk_id,
                    "relevance": round(r.relevance_score, 3),
                    "match_count": r.match_count,
                    "content": r.content[:2000] + "..." if len(r.content) > 2000 else r.content,
                    "position": {"start": r.start_char, "end": r.end_char}
                }
                for r in results
            ],
            "can_search_deeper": depth < self.max_depth,
            "hint": "Use 'rlm_search_recursive' on specific chunks to go deeper into relevant sections."
        }
    
    async def search_recursive(self, query: str, chunk_ids: list[int],
                              context_id: str = None, 
                              parent_query_id: str = None) -> dict:
        """
        Perform recursive sub-search on specific chunks.
        
        This is the key RLM innovation: the model can recursively dive into
        sections it found relevant, searching deeper for specific information.
        """
        context_id = context_id or self.active_session
        if not context_id or context_id not in self.contexts:
            return {"error": "No context loaded."}
        
        context = self.contexts[context_id]
        
        # Get the specified chunks
        selected_chunks = [c for c in context.chunks if c["id"] in chunk_ids]
        if not selected_chunks:
            return {"error": "No valid chunks found with given IDs."}
        
        # Combine chunks into a sub-context
        combined_content = '\n\n---CHUNK_BOUNDARY---\n\n'.join(
            c["content"] for c in selected_chunks
        )
        
        # Create temporary sub-context
        sub_context_id = f"sub_{context_id}_{self.generate_id(combined_content)[:6]}"
        sub_chunks = self.chunk_content(combined_content)
        
        sub_context = ContextStore(
            id=sub_context_id,
            name=f"sub-context of {context.name}",
            content=combined_content,
            token_estimate=self.estimate_tokens(combined_content),
            created_at=datetime.now().isoformat(),
            metadata={"parent_context": context_id, "source_chunks": chunk_ids},
            chunks=sub_chunks
        )
        
        self.contexts[sub_context_id] = sub_context
        
        # Perform search on sub-context
        result = await self.search_context(
            query=query,
            context_id=sub_context_id,
            parent_query_id=parent_query_id
        )
        
        result["recursive_info"] = {
            "source_chunks": chunk_ids,
            "sub_context_tokens": sub_context.token_estimate,
            "is_recursive": True
        }
        
        return result
    
    async def get_chunk(self, chunk_id: int, context_id: str = None,
                       with_context: bool = True) -> dict:
        """
        Retrieve a specific chunk with optional surrounding context.
        
        Useful for examining specific sections found during search.
        """
        context_id = context_id or self.active_session
        if not context_id or context_id not in self.contexts:
            return {"error": "No context loaded."}
        
        context = self.contexts[context_id]
        
        if chunk_id < 0 or chunk_id >= len(context.chunks):
            return {"error": f"Invalid chunk ID. Valid range: 0-{len(context.chunks)-1}"}
        
        chunk = context.chunks[chunk_id]
        
        result = {
            "chunk_id": chunk_id,
            "content": chunk["content"],
            "tokens": chunk["tokens"],
            "position": {
                "start_char": chunk["start_char"],
                "end_char": chunk["end_char"]
            }
        }
        
        if with_context:
            if chunk_id > 0:
                result["previous_chunk_preview"] = context.chunks[chunk_id - 1]["content"][-500:]
            if chunk_id < len(context.chunks) - 1:
                result["next_chunk_preview"] = context.chunks[chunk_id + 1]["content"][:500]
        
        return result
    
    async def list_contexts(self) -> dict:
        """List all loaded contexts."""
        return {
            "contexts": [
                {
                    "id": ctx.id,
                    "name": ctx.name,
                    "tokens": ctx.token_estimate,
                    "chunks": len(ctx.chunks),
                    "created_at": ctx.created_at
                }
                for ctx in self.contexts.values()
            ],
            "active_session": self.active_session,
            "stats": self.stats
        }
    
    async def get_outline(self, context_id: str = None, max_depth: int = 3) -> dict:
        """
        Generate a structural outline of the context.
        
        Identifies headers, sections, and logical divisions to help
        navigate large documents.
        """
        context_id = context_id or self.active_session
        if not context_id or context_id not in self.contexts:
            return {"error": "No context loaded."}
        
        context = self.contexts[context_id]
        
        # Extract structure indicators
        outline = []
        header_patterns = [
            (r'^#{1,6}\s+(.+)$', 'markdown'),
            (r'^(Chapter|Section|Part)\s+(\d+):?\s*(.+)$', 'book'),
            (r'^(def|class|async def)\s+(\w+)', 'code'),
            (r'^<h[1-6][^>]*>(.+)</h[1-6]>', 'html'),
        ]
        
        for chunk in context.chunks:
            for pattern, pattern_type in header_patterns:
                matches = re.finditer(pattern, chunk["content"], re.MULTILINE)
                for match in matches:
                    level = 1
                    if pattern_type == 'markdown':
                        level = len(match.group(0).split()[0])
                    
                    if level <= max_depth:
                        outline.append({
                            "title": match.group(1)[:100] if match.groups() else match.group(0)[:100],
                            "type": pattern_type,
                            "level": level,
                            "chunk_id": chunk["id"],
                            "position": chunk["start_char"] + match.start()
                        })
        
        return {
            "context_id": context_id,
            "context_name": context.name,
            "total_tokens": context.token_estimate,
            "outline_items": len(outline),
            "outline": outline[:100]  # Limit for response size
        }
    
    async def get_statistics(self) -> dict:
        """Get RLM session statistics."""
        query_depths = defaultdict(int)
        for q in self.queries.values():
            query_depths[q.depth] += 1
        
        return {
            "session_stats": self.stats,
            "query_depth_distribution": dict(query_depths),
            "active_contexts": len(self.contexts),
            "total_tokens_in_memory": sum(c.token_estimate for c in self.contexts.values()),
            "configuration": {
                "max_depth": self.max_depth,
                "chunk_size": self.chunk_size,
                "overlap": self.overlap
            }
        }
    
    async def clear_context(self, context_id: str = None) -> dict:
        """Clear a specific context or all contexts."""
        if context_id:
            if context_id in self.contexts:
                del self.contexts[context_id]
                if self.active_session == context_id:
                    self.active_session = None
                return {"success": True, "cleared": context_id}
            return {"error": "Context not found."}
        else:
            count = len(self.contexts)
            self.contexts.clear()
            self.active_session = None
            return {"success": True, "cleared_count": count}


# === MCP Protocol Implementation ===

async def handle_request(server: RLMServer, request: dict) -> dict:
    """Handle incoming MCP requests."""
    method = request.get("method", "")
    params = request.get("params", {})
    request_id = request.get("id")
    
    try:
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "rlm-infinite-context",
                        "version": "1.0.0"
                    }
                }
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "rlm_load",
                            "description": "Load a large context into RLM storage for recursive searching. The context is chunked and indexed for efficient searching across millions of tokens.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "content": {"type": "string", "description": "The full content to load (can be millions of tokens)"},
                                    "name": {"type": "string", "description": "Name for this context", "default": "default"},
                                    "metadata": {"type": "object", "description": "Optional metadata about the content"}
                                },
                                "required": ["content"]
                            }
                        },
                        {
                            "name": "rlm_search",
                            "description": "Search through loaded context. Supports regex, keyword, and semantic section search. Returns relevant chunks without loading entire context into model.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string", "description": "Search query (keywords, regex pattern, or section name)"},
                                    "context_id": {"type": "string", "description": "Context to search (uses active session if not specified)"},
                                    "search_type": {"type": "string", "enum": ["auto", "regex", "keyword", "section"], "default": "auto"},
                                    "top_k": {"type": "integer", "description": "Number of results to return", "default": 5},
                                    "parent_query_id": {"type": "string", "description": "ID of parent query for recursive searching"}
                                },
                                "required": ["query"]
                            }
                        },
                        {
                            "name": "rlm_search_recursive",
                            "description": "Perform recursive sub-search on specific chunks. This is the key RLM feature - dive deeper into relevant sections found in initial search.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string", "description": "What to search for within the selected chunks"},
                                    "chunk_ids": {"type": "array", "items": {"type": "integer"}, "description": "IDs of chunks to search within"},
                                    "context_id": {"type": "string", "description": "Context ID"},
                                    "parent_query_id": {"type": "string", "description": "ID of the search that found these chunks"}
                                },
                                "required": ["query", "chunk_ids"]
                            }
                        },
                        {
                            "name": "rlm_get_chunk",
                            "description": "Retrieve a specific chunk with optional surrounding context.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "chunk_id": {"type": "integer", "description": "ID of chunk to retrieve"},
                                    "context_id": {"type": "string", "description": "Context ID"},
                                    "with_context": {"type": "boolean", "description": "Include previews of adjacent chunks", "default": True}
                                },
                                "required": ["chunk_id"]
                            }
                        },
                        {
                            "name": "rlm_outline",
                            "description": "Generate structural outline of context (headers, sections, functions). Helps navigate large documents.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "context_id": {"type": "string", "description": "Context ID"},
                                    "max_depth": {"type": "integer", "description": "Maximum heading depth to include", "default": 3}
                                }
                            }
                        },
                        {
                            "name": "rlm_list",
                            "description": "List all loaded contexts and session statistics.",
                            "inputSchema": {"type": "object", "properties": {}}
                        },
                        {
                            "name": "rlm_stats",
                            "description": "Get detailed RLM session statistics including query depth distribution and token usage.",
                            "inputSchema": {"type": "object", "properties": {}}
                        },
                        {
                            "name": "rlm_clear",
                            "description": "Clear loaded contexts to free memory.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "context_id": {"type": "string", "description": "Specific context to clear (clears all if not specified)"}
                                }
                            }
                        }
                    ]
                }
            }
        
        elif method == "tools/call":
            tool_name = params.get("name", "")
            tool_args = params.get("arguments", {})
            
            if tool_name == "rlm_load":
                result = await server.load_context(**tool_args)
            elif tool_name == "rlm_search":
                result = await server.search_context(**tool_args)
            elif tool_name == "rlm_search_recursive":
                result = await server.search_recursive(**tool_args)
            elif tool_name == "rlm_get_chunk":
                result = await server.get_chunk(**tool_args)
            elif tool_name == "rlm_outline":
                result = await server.get_outline(**tool_args)
            elif tool_name == "rlm_list":
                result = await server.list_contexts()
            elif tool_name == "rlm_stats":
                result = await server.get_statistics()
            elif tool_name == "rlm_clear":
                result = await server.clear_context(**tool_args)
            else:
                result = {"error": f"Unknown tool: {tool_name}"}
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            }
        
        elif method == "notifications/initialized":
            return None  # No response needed for notifications
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }
            
    except Exception as e:
        logger.exception(f"Error handling request: {e}")
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32603, "message": str(e)}
        }


async def main():
    """Main entry point for MCP server."""
    server = RLMServer()
    logger.info("RLM MCP Server starting...")
    
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin)
    
    writer_transport, writer_protocol = await asyncio.get_event_loop().connect_write_pipe(
        asyncio.streams.FlowControlMixin, sys.stdout
    )
    writer = asyncio.StreamWriter(writer_transport, writer_protocol, None, asyncio.get_event_loop())
    
    while True:
        try:
            line = await reader.readline()
            if not line:
                break
            
            request = json.loads(line.decode())
            response = await handle_request(server, request)
            
            if response:
                response_bytes = (json.dumps(response) + "\n").encode()
                writer.write(response_bytes)
                await writer.drain()
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
        except Exception as e:
            logger.exception(f"Error in main loop: {e}")


if __name__ == "__main__":
    asyncio.run(main())
