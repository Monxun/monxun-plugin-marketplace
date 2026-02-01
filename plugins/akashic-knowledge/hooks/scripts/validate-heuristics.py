#!/usr/bin/env python3
"""
Post-discovery heuristic validation hook for Akashic Knowledge plugin.

Validates discovered heuristics after AutoHD pipeline:
- Checks heuristic format
- Validates metadata
- Reports quality metrics

Exit codes:
- 0: Validation passed
- 1: Non-blocking warnings
"""

import json
import os
import sys
from pathlib import Path


def validate_heuristic_format(heuristic_data: dict) -> list[str]:
    """Validate heuristic data format."""
    errors = []

    required_fields = ["status", "kb_name", "domain"]
    for field in required_fields:
        if field not in heuristic_data:
            errors.append(f"Missing required field: {field}")

    return errors


def check_quality_metrics(heuristic_data: dict) -> dict:
    """Check quality metrics from discovery result."""
    metrics = {
        "passed": True,
        "warnings": [],
        "recommendations": [],
    }

    # Check if discovery was initiated successfully
    if heuristic_data.get("status") == "discovery_initiated":
        metrics["recommendations"].append(
            "Discovery initiated. Run the full pipeline with orchestrator agent."
        )
    elif heuristic_data.get("status") == "completed":
        # Check performance metrics if available
        performance = heuristic_data.get("performance", {})

        if performance.get("accuracy", 0) < 0.85:
            metrics["warnings"].append(
                f"Accuracy below threshold: {performance.get('accuracy', 'N/A')}"
            )

        if performance.get("e_value", 0) < 20:
            metrics["warnings"].append(
                f"E-value below significance threshold: {performance.get('e_value', 'N/A')}"
            )

    return metrics


def log_discovery_result(heuristic_data: dict) -> None:
    """Log discovery result for tracking."""
    log_dir = Path(os.getenv("AKASHIC_DATA_DIR", Path.home() / ".akashic")) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    from datetime import datetime

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "heuristic_discovery",
        "kb_name": heuristic_data.get("kb_name"),
        "domain": heuristic_data.get("domain"),
        "status": heuristic_data.get("status"),
    }

    log_file = log_dir / "discoveries.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def main():
    """Main entry point."""
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Failed to parse hook input", file=sys.stderr)
        sys.exit(1)

    tool_result = hook_input.get("tool_result", {})

    # Parse the result
    try:
        result_data = json.loads(tool_result.get("content", "{}"))
    except json.JSONDecodeError:
        result_data = {}

    # Validate format
    format_errors = validate_heuristic_format(result_data)
    if format_errors:
        print("Format validation errors:")
        for error in format_errors:
            print(f"  - {error}")

    # Check quality
    quality = check_quality_metrics(result_data)

    print(f"\nHeuristic Discovery: {result_data.get('status', 'unknown')}")
    print(f"Domain: {result_data.get('domain', 'unknown')}")
    print(f"Knowledge Base: {result_data.get('kb_name', 'unknown')}")

    if quality["warnings"]:
        print("\nWarnings:")
        for w in quality["warnings"]:
            print(f"  - {w}")

    if quality["recommendations"]:
        print("\nRecommendations:")
        for r in quality["recommendations"]:
            print(f"  - {r}")

    # Log the result
    log_discovery_result(result_data)

    sys.exit(0 if quality["passed"] else 1)


if __name__ == "__main__":
    main()
