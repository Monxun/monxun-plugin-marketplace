#!/usr/bin/env python3
"""
Validate Python heuristic function syntax.

Exit codes:
- 0: Success (valid syntax)
- 1: Warning (non-blocking issues)
- 2: Block (invalid syntax, stop operation)
"""

import sys
import json
import ast

def validate_heuristic_file(file_path: str) -> dict:
    """Validate a Python heuristic file."""
    issues = []

    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Parse AST
        tree = ast.parse(content)

        # Find heuristic functions
        heuristic_functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith('heuristic'):
                    heuristic_functions.append(node)

        if not heuristic_functions:
            issues.append({
                "severity": "warning",
                "message": "No heuristic function found (expected function starting with 'heuristic')"
            })

        for func in heuristic_functions:
            # Check for return type annotation
            if func.returns is None:
                issues.append({
                    "severity": "warning",
                    "message": f"Function '{func.name}' missing return type annotation (expected -> float)"
                })

            # Check for docstring
            if not ast.get_docstring(func):
                issues.append({
                    "severity": "warning",
                    "message": f"Function '{func.name}' missing docstring"
                })

            # Check argument count
            args = func.args.args
            if len(args) < 2:
                issues.append({
                    "severity": "error",
                    "message": f"Function '{func.name}' needs at least 2 arguments (current_state, goal_state)"
                })

        # Check for HEURISTIC_METADATA
        has_metadata = any(
            isinstance(node, ast.Assign) and
            any(isinstance(t, ast.Name) and t.id == 'HEURISTIC_METADATA' for t in node.targets)
            for node in ast.walk(tree)
        )

        if not has_metadata:
            issues.append({
                "severity": "info",
                "message": "Consider adding HEURISTIC_METADATA dict for framework integration"
            })

    except SyntaxError as e:
        issues.append({
            "severity": "error",
            "message": f"Syntax error: {e.msg} at line {e.lineno}"
        })
    except Exception as e:
        issues.append({
            "severity": "error",
            "message": f"Validation error: {str(e)}"
        })

    return {
        "file": file_path,
        "issues": issues,
        "valid": not any(i["severity"] == "error" for i in issues)
    }


def main():
    # Read hook input from stdin
    input_data = json.loads(sys.stdin.read())

    file_path = input_data.get("tool_input", {}).get("file_path", "")

    if not file_path.endswith('.py'):
        # Not a Python file, skip
        sys.exit(0)

    result = validate_heuristic_file(file_path)

    # Output validation result
    if result["issues"]:
        for issue in result["issues"]:
            print(f"[{issue['severity'].upper()}] {issue['message']}", file=sys.stderr)

    # Determine exit code
    if not result["valid"]:
        sys.exit(2)  # Block - has errors
    elif any(i["severity"] == "warning" for i in result["issues"]):
        sys.exit(1)  # Warning - non-blocking
    else:
        sys.exit(0)  # Success


if __name__ == "__main__":
    main()
