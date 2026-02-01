#!/usr/bin/env python3
"""
Usage tracking hook for RLM search operations.
Tracks token usage and search patterns for optimization.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def main():
    """Track RLM search usage."""
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)
    
    # Extract usage data
    tool_name = input_data.get("tool_name", "unknown")
    tool_input = input_data.get("tool_input", {})
    tool_response = input_data.get("tool_response", {})
    
    # Parse response if it's a string
    if isinstance(tool_response, str):
        try:
            tool_response = json.loads(tool_response)
        except json.JSONDecodeError:
            tool_response = {}
    
    # If response has content array, extract text
    if isinstance(tool_response, dict) and "content" in tool_response:
        content = tool_response.get("content", [])
        if content and isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    try:
                        tool_response = json.loads(item.get("text", "{}"))
                    except json.JSONDecodeError:
                        pass
                    break
    
    # Track metrics
    usage = {
        "timestamp": datetime.now().isoformat(),
        "tool": tool_name,
        "query": tool_input.get("query", ""),
        "search_type": tool_input.get("search_type", "auto"),
        "results": tool_response.get("result_count", 0),
        "tokens": tool_response.get("tokens_returned", 0),
        "depth": tool_response.get("depth", 0)
    }
    
    # Log to stderr
    print(f"RLM Search: {usage['results']} results, {usage['tokens']} tokens, depth {usage['depth']}", file=sys.stderr)
    
    # Optionally append to usage log
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", ".")
    log_file = Path(plugin_root) / "data" / "usage.log"
    
    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(json.dumps(usage) + '\n')
    except Exception as e:
        print(f"Warning: Could not write usage log: {e}", file=sys.stderr)
    
    # Output for context injection
    output = {
        "usage_tracked": True,
        "metrics": usage
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
