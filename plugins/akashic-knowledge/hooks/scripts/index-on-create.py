#!/usr/bin/env python3
"""
Post-create indexing hook for Akashic Knowledge plugin.

Automatically sets up indices and configurations after KB creation:
- Logs creation event
- Prepares index configurations
- Validates infrastructure connectivity

Exit codes:
- 0: Success
- 1: Non-blocking warning
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def log_creation(tool_result: dict, kb_info: dict) -> None:
    """Log knowledge base creation event."""
    log_dir = Path(os.getenv("AKASHIC_DATA_DIR", Path.home() / ".akashic")) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "kb_created",
        "kb_name": kb_info.get("name", "unknown"),
        "scope": kb_info.get("scope", "unknown"),
        "collections": kb_info.get("collections", []),
        "result": tool_result,
    }

    log_file = log_dir / "events.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def check_infrastructure() -> list[str]:
    """Check infrastructure connectivity."""
    warnings = []

    # Check if Docker is available
    import subprocess

    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        running_containers = result.stdout.strip().split("\n")

        expected = ["akashic-qdrant", "akashic-neo4j", "akashic-elasticsearch"]
        for container in expected:
            if container not in running_containers:
                warnings.append(f"Container not running: {container}")

    except (subprocess.TimeoutExpired, FileNotFoundError):
        warnings.append("Docker not available or timed out")

    return warnings


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

    if result_data.get("success"):
        kb_info = result_data.get("kb", {})
        log_creation(tool_result, kb_info)

        print(f"Knowledge base '{kb_info.get('name')}' created successfully.")
        print(f"Scope: {kb_info.get('scope')}")
        print(f"Collections: {', '.join(kb_info.get('collections', []))}")

        # Check infrastructure
        warnings = check_infrastructure()
        if warnings:
            print("\nInfrastructure warnings:")
            for w in warnings:
                print(f"  - {w}")

    sys.exit(0)


if __name__ == "__main__":
    main()
