#!/usr/bin/env python3
"""
Validate JSON-LD heuristic schema compliance.

Exit codes:
- 0: Success (valid schema)
- 1: Warning (non-blocking issues)
- 2: Block (invalid schema)
"""

import sys
import json

REQUIRED_FIELDS = ["@type", "@id", "name", "description"]
RECOMMENDED_FIELDS = ["heuristic:confidence", "popper:validation", "heuristic:domain"]

def validate_jsonld(content: dict) -> dict:
    """Validate JSON-LD heuristic document."""
    issues = []

    # Check @context
    if "@context" not in content:
        issues.append({
            "severity": "warning",
            "message": "Missing @context - document may not be fully JSON-LD compliant"
        })

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in content:
            issues.append({
                "severity": "error",
                "message": f"Missing required field: {field}"
            })

    # Check @type
    if content.get("@type") and "Heuristic" not in str(content["@type"]):
        issues.append({
            "severity": "warning",
            "message": f"@type should include 'Heuristic', found: {content.get('@type')}"
        })

    # Check recommended fields
    for field in RECOMMENDED_FIELDS:
        if field not in content:
            issues.append({
                "severity": "info",
                "message": f"Consider adding recommended field: {field}"
            })

    # Validate confidence range
    confidence = content.get("heuristic:confidence") or content.get("confidence")
    if confidence is not None:
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            issues.append({
                "severity": "error",
                "message": f"Confidence must be between 0 and 1, got: {confidence}"
            })

    # Validate validation section
    validation = content.get("popper:validation") or content.get("validation")
    if validation:
        if "method" not in validation:
            issues.append({
                "severity": "warning",
                "message": "Validation section missing 'method' field"
            })
        if validation.get("typeIError"):
            error_rate = validation["typeIError"]
            if not 0 < error_rate < 1:
                issues.append({
                    "severity": "error",
                    "message": f"Type-I error rate must be between 0 and 1, got: {error_rate}"
                })

    return {
        "issues": issues,
        "valid": not any(i["severity"] == "error" for i in issues)
    }


def main():
    # Read hook input from stdin
    input_data = json.loads(sys.stdin.read())

    file_path = input_data.get("tool_input", {}).get("file_path", "")

    if not file_path.endswith('.jsonld'):
        sys.exit(0)

    try:
        with open(file_path, 'r') as f:
            content = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON: {e}", file=sys.stderr)
        sys.exit(2)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}", file=sys.stderr)
        sys.exit(2)

    result = validate_jsonld(content)

    # Output validation result
    if result["issues"]:
        for issue in result["issues"]:
            print(f"[{issue['severity'].upper()}] {issue['message']}", file=sys.stderr)

    # Determine exit code
    if not result["valid"]:
        sys.exit(2)
    elif any(i["severity"] == "warning" for i in result["issues"]):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
