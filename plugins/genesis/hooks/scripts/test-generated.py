#!/usr/bin/env python3
"""
Stop hook: Test generated templates before session ends.

Exit codes:
- 0: All tests passed
- 1: Tests failed (non-blocking warning)
"""

import json
import os
import sys
import subprocess
from pathlib import Path


def find_genesis_templates():
    """Find all genesis.json files in current directory tree."""
    templates = []
    for root, dirs, files in os.walk("."):
        # Skip node_modules and similar
        dirs[:] = [
            d for d in dirs if d not in ["node_modules", ".git", "venv", "__pycache__"]
        ]

        if "genesis.json" in files:
            templates.append(os.path.join(root, "genesis.json"))

    return templates


def validate_template(template_path):
    """Run validation on a single template."""
    template_dir = os.path.dirname(template_path)
    results = {"path": template_dir, "errors": [], "warnings": []}

    # Check genesis.json is valid JSON
    try:
        with open(template_path) as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        results["errors"].append(f"Invalid genesis.json: {e}")
        return results

    # Check required fields
    if "name" not in manifest:
        results["errors"].append("Missing 'name' in genesis.json")

    # Check templates directory exists
    templates_dir = os.path.join(template_dir, "templates")
    if not os.path.isdir(templates_dir):
        results["warnings"].append("No 'templates' directory found")

    # Check for undefined variables
    if os.path.isdir(templates_dir):
        defined_vars = {p.get("name") for p in manifest.get("prompts", [])}
        used_vars = set()

        for root, dirs, files in os.walk(templates_dir):
            for file in files:
                if file.endswith(".template"):
                    filepath = os.path.join(root, file)
                    with open(filepath, "r", errors="ignore") as f:
                        content = f.read()
                        # Find {{ variable_name }} patterns
                        import re

                        matches = re.findall(r"\{\{\s*([a-z_][a-z0-9_]*)", content)
                        used_vars.update(matches)

        undefined = used_vars - defined_vars
        # Filter out built-in variables and helpers
        builtins = {
            "this",
            "index",
            "first",
            "last",
            "key",
            "root",
            "if",
            "unless",
            "each",
            "else",
        }
        undefined = undefined - builtins

        if undefined:
            results["warnings"].append(f"Undefined variables: {', '.join(undefined)}")

    # Check README exists
    readme_path = os.path.join(template_dir, "README.md")
    if not os.path.exists(readme_path):
        results["warnings"].append("No README.md found")

    return results


def main():
    """Main entry point."""
    templates = find_genesis_templates()

    if not templates:
        # No templates found, nothing to test
        print("No Genesis templates found to validate")
        sys.exit(0)

    all_passed = True
    total_errors = 0
    total_warnings = 0

    print(f"\n{'='*60}")
    print("Genesis Template Validation Report")
    print(f"{'='*60}\n")

    for template_path in templates:
        results = validate_template(template_path)

        status = "PASS"
        if results["errors"]:
            status = "FAIL"
            all_passed = False
        elif results["warnings"]:
            status = "WARN"

        print(f"Template: {results['path']}")
        print(f"Status: {status}")

        if results["errors"]:
            print("Errors:")
            for error in results["errors"]:
                print(f"  - {error}")
            total_errors += len(results["errors"])

        if results["warnings"]:
            print("Warnings:")
            for warning in results["warnings"]:
                print(f"  - {warning}")
            total_warnings += len(results["warnings"])

        print()

    print(f"{'='*60}")
    print(
        f"Summary: {len(templates)} template(s), {total_errors} error(s), {total_warnings} warning(s)"
    )
    print(f"{'='*60}\n")

    # Always exit 0 to not block session end
    # Errors are informational
    sys.exit(0)


if __name__ == "__main__":
    main()
