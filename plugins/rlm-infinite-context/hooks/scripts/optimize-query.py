#!/usr/bin/env python3
"""
Query optimization hook for RLM search operations.
Enhances queries for better search results.
"""

import json
import re
import sys


def optimize_query(query: str, search_type: str) -> dict:
    """Optimize search query."""
    optimizations = []
    optimized_query = query
    
    if search_type == "keyword":
        # Remove common stop words for keyword search
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 
                     'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                     'would', 'could', 'should', 'may', 'might', 'must', 'shall'}
        
        words = query.lower().split()
        filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
        
        if len(filtered_words) < len(words):
            optimizations.append(f"Removed {len(words) - len(filtered_words)} stop words")
            optimized_query = ' '.join(filtered_words)
    
    elif search_type == "regex":
        # Validate regex
        try:
            re.compile(query)
        except re.error as e:
            return {
                "valid": False,
                "error": f"Invalid regex: {e}",
                "suggestion": "Check regex syntax"
            }
        
        # Add word boundaries if searching for specific terms
        if re.match(r'^[a-zA-Z_]\w*$', query):
            optimized_query = rf'\b{query}\b'
            optimizations.append("Added word boundaries")
    
    return {
        "valid": True,
        "original": query,
        "optimized": optimized_query,
        "optimizations": optimizations,
        "search_type": search_type
    }


def main():
    """Optimize RLM search query."""
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # No input, continue without optimization
        sys.exit(0)
    
    # Get search parameters
    tool_input = input_data.get("tool_input", {})
    arguments = input_data.get("arguments", tool_input)
    query = arguments.get("query", "")
    search_type = arguments.get("search_type", "auto")
    
    if not query:
        sys.exit(0)
    
    # Optimize
    result = optimize_query(query, search_type)
    
    if not result["valid"]:
        print(f"Query error: {result['error']}", file=sys.stderr)
        # Don't block, just warn
    
    # Log optimizations
    if result.get("optimizations"):
        print(f"Query optimizations: {', '.join(result['optimizations'])}", file=sys.stderr)
    
    # Output result
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
