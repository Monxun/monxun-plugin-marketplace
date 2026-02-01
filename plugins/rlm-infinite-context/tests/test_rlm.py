#!/usr/bin/env python3
"""
Test script for RLM Infinite Context Plugin.
Verifies core functionality works correctly.
"""

import asyncio
import sys
import os

# Add servers to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'servers'))

from rlm_server import RLMServer


async def test_basic_workflow():
    """Test basic RLM workflow."""
    print("=" * 60)
    print("RLM Infinite Context Plugin - Test Suite")
    print("=" * 60)
    
    server = RLMServer()
    
    # Test 1: Load context
    print("\n[Test 1] Loading context...")
    test_content = """
# Chapter 1: Introduction

This is a test document for the RLM infinite context plugin.
The plugin implements recursive language model techniques.

## Section 1.1: Background

Traditional LLMs have limited context windows. As context grows,
quality degrades due to context rot. RLM solves this by storing
content externally and providing search tools.

## Section 1.2: Key Features

- Unlimited context length
- No information loss
- Recursive search capability
- Cost efficient

# Chapter 2: Implementation

The implementation uses chunking and indexing for efficient search.

## Section 2.1: Chunking Strategy

Content is split into overlapping chunks of approximately 4000 characters.
This allows for semantic boundary preservation while maintaining searchability.

def chunk_content(content, chunk_size=4000, overlap=200):
    # Implementation details here
    pass

## Section 2.2: Search Types

Three main search types are supported:
1. Keyword search - finds matching terms
2. Regex search - pattern matching
3. Section search - finds document structure

# Chapter 3: Usage

Load content with rlm_load, then search with rlm_search.

## Section 3.1: Examples

Example usage:
- Load a document: rlm_load(content)
- Search: rlm_search("authentication")
- Deep search: rlm_search_recursive("OAuth", chunk_ids=[1,2,3])
"""
    
    result = await server.load_context(test_content, "test-document")
    print(f"  ✓ Loaded {result['token_estimate']} tokens in {result['chunk_count']} chunks")
    assert result['success'] == True
    assert result['chunk_count'] > 0
    
    # Test 2: Get outline
    print("\n[Test 2] Getting outline...")
    outline = await server.get_outline()
    print(f"  ✓ Found {outline['outline_items']} outline items")
    assert outline['outline_items'] > 0
    
    # Test 3: Keyword search
    print("\n[Test 3] Keyword search...")
    results = await server.search_context("authentication OAuth", search_type="keyword")
    print(f"  ✓ Found {results['result_count']} results")
    assert results['result_count'] > 0
    
    # Test 4: Regex search
    print("\n[Test 4] Regex search...")
    results = await server.search_context(r"def\s+\w+", search_type="regex")
    print(f"  ✓ Found {results['result_count']} results with regex")
    assert results['result_count'] > 0
    
    # Test 5: Section search
    print("\n[Test 5] Section search...")
    results = await server.search_context("Chapter", search_type="section")
    print(f"  ✓ Found {results['result_count']} sections")
    assert results['result_count'] > 0
    
    # Test 6: Recursive search
    print("\n[Test 6] Recursive search...")
    initial = await server.search_context("Implementation")
    if initial['result_count'] > 0:
        chunk_ids = [r['chunk_id'] for r in initial['results'][:2]]
        recursive = await server.search_recursive(
            "chunking", 
            chunk_ids,
            parent_query_id=initial['query_id']
        )
        print(f"  ✓ Recursive search found {recursive['result_count']} results at depth {recursive['depth']}")
        assert recursive['depth'] > 0
    
    # Test 7: Get chunk
    print("\n[Test 7] Get specific chunk...")
    chunk = await server.get_chunk(0)
    print(f"  ✓ Retrieved chunk with {chunk['tokens']} tokens")
    assert 'content' in chunk
    
    # Test 8: Statistics
    print("\n[Test 8] Get statistics...")
    stats = await server.get_statistics()
    print(f"  ✓ Total queries: {stats['session_stats']['total_queries']}")
    assert stats['session_stats']['total_queries'] > 0
    
    # Test 9: List contexts
    print("\n[Test 9] List contexts...")
    contexts = await server.list_contexts()
    print(f"  ✓ Active contexts: {len(contexts['contexts'])}")
    assert len(contexts['contexts']) > 0
    
    # Test 10: Clear
    print("\n[Test 10] Clear contexts...")
    clear_result = await server.clear_context()
    print(f"  ✓ Cleared {clear_result['cleared_count']} contexts")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_basic_workflow())
