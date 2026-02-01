"""
RLM (Recursive Language Model) MCP Server Package

Implements MIT's RLM technique for infinite context processing.
"""

from .rlm_server import RLMServer, ContextStore, SearchResult, RecursiveQuery

__all__ = ["RLMServer", "ContextStore", "SearchResult", "RecursiveQuery"]
__version__ = "1.0.0"
