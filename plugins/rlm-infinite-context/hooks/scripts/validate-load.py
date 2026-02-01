#!/usr/bin/env python3
"""
Pre-load validation hook for RLM plugin.
Validates content before loading into RLM storage.
"""

import json
import sys


def estimate_tokens(content: str) -> int:
    """Estimate token count."""
    return len(content) // 4


def validate_content(content: str) -> dict:
    """Validate content for RLM loading."""
    issues = []
    warnings = []
    
    # Check if content exists
    if not content or len(content.strip()) == 0:
        issues.append("Content is empty")
        return {"valid": False, "issues": issues, "warnings": warnings}
    
    # Check size
    tokens = estimate_tokens(content)
    
    if tokens < 100:
        warnings.append(f"Content is very short ({tokens} tokens). RLM is optimized for large contexts.")
    
    if tokens > 50_000_000:  # 50M tokens
        warnings.append(f"Content is extremely large ({tokens:,} tokens). This may impact performance.")
    
    # Check for binary content
    try:
        content.encode('utf-8')
    except UnicodeError:
        issues.append("Content contains invalid UTF-8 characters")
    
    # Check for potential issues
    null_count = content.count('\x00')
    if null_count > 0:
        warnings.append(f"Content contains {null_count} null bytes")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "stats": {
            "length": len(content),
            "estimated_tokens": tokens,
            "lines": content.count('\n') + 1
        }
    }


def main():
    """Validate RLM load operation."""
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Get tool input
    tool_input = input_data.get("tool_input", {})
    arguments = input_data.get("arguments", tool_input)
    content = arguments.get("content", "")
    
    # Validate
    result = validate_content(content)
    
    if not result["valid"]:
        # Block the operation
        print(f"RLM Load blocked: {', '.join(result['issues'])}", file=sys.stderr)
        sys.exit(2)  # Exit 2 = block
    
    # Log warnings
    for warning in result["warnings"]:
        print(f"RLM Warning: {warning}", file=sys.stderr)
    
    # Log stats
    stats = result["stats"]
    print(f"RLM Load validated: {stats['estimated_tokens']:,} tokens, {stats['lines']:,} lines", file=sys.stderr)
    
    # Success - continue with operation
    output = {
        "validated": True,
        "stats": stats
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
