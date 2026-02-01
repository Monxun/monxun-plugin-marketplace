#!/usr/bin/env python3
"""
Stop hook: Enforce quality gates at session end.

Runs comprehensive validation and reports quality score.

Exit codes:
- 0: All gates passed
- 2: Critical failures (blocks if in strict mode)
"""

import json
import sys
import os
from pathlib import Path
import subprocess
import re

def get_plugin_root() -> Path:
    """Get plugin root directory."""
    return Path(os.environ.get('CLAUDE_PLUGIN_ROOT', Path(__file__).parent.parent.parent))

def check_structure(plugin_path: Path) -> tuple[bool, list]:
    """Gate 1: Structure validation."""
    errors = []

    # Check .claude-plugin/plugin.json exists
    manifest = plugin_path / '.claude-plugin' / 'plugin.json'
    if not manifest.exists():
        errors.append("Missing .claude-plugin/plugin.json")

    # Check only plugin.json in .claude-plugin/
    claude_plugin_dir = plugin_path / '.claude-plugin'
    if claude_plugin_dir.exists():
        contents = list(claude_plugin_dir.iterdir())
        non_manifest = [f.name for f in contents if f.name != 'plugin.json']
        if non_manifest:
            errors.append(f"Extra files in .claude-plugin/: {non_manifest}")

    # Check components at root
    for component in ['commands', 'agents', 'skills']:
        component_path = plugin_path / component
        if component_path.exists() and not component_path.is_dir():
            errors.append(f"{component} should be a directory at root")

    return len(errors) == 0, errors

def check_schema(plugin_path: Path) -> tuple[bool, list]:
    """Gate 2: Schema validation."""
    errors = []

    # Validate plugin.json
    manifest = plugin_path / '.claude-plugin' / 'plugin.json'
    if manifest.exists():
        try:
            with open(manifest) as f:
                data = json.load(f)

            # Check required fields
            required = ['name', 'version', 'description']
            for field in required:
                if field not in data:
                    errors.append(f"plugin.json missing '{field}'")

            # Check name format
            name = data.get('name', '')
            if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
                errors.append(f"Name not kebab-case: {name}")

        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in plugin.json: {e}")

    # Validate hooks.json if exists
    hooks_file = plugin_path / 'hooks' / 'hooks.json'
    if hooks_file.exists():
        try:
            with open(hooks_file) as f:
                json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in hooks.json: {e}")

    return len(errors) == 0, errors

def check_components(plugin_path: Path) -> tuple[bool, list]:
    """Gate 3: Component validation."""
    errors = []

    # Check skill files
    skills_dir = plugin_path / 'skills'
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_md = skill_dir / 'SKILL.md'
                if not skill_md.exists():
                    errors.append(f"Missing SKILL.md in {skill_dir.name}")
                else:
                    # Check frontmatter
                    with open(skill_md) as f:
                        content = f.read()
                    if not content.startswith('---'):
                        errors.append(f"{skill_dir.name}/SKILL.md missing frontmatter")

    # Check agent files
    agents_dir = plugin_path / 'agents'
    if agents_dir.exists():
        for agent_file in agents_dir.glob('*.md'):
            with open(agent_file) as f:
                content = f.read()
            if not content.startswith('---'):
                errors.append(f"agents/{agent_file.name} missing frontmatter")

    return len(errors) == 0, errors

def check_quality(plugin_path: Path) -> tuple[bool, list]:
    """Gate 4: Quality validation."""
    errors = []
    warnings = []

    # Check SKILL.md line counts
    skills_dir = plugin_path / 'skills'
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_md = skill_dir / 'SKILL.md'
                if skill_md.exists():
                    with open(skill_md) as f:
                        lines = f.read().count('\n') + 1
                    if lines > 500:
                        errors.append(f"{skill_dir.name}/SKILL.md has {lines} lines (max 500)")
                    elif lines > 400:
                        warnings.append(f"{skill_dir.name}/SKILL.md has {lines} lines (approaching limit)")

    return len(errors) == 0, errors + warnings

def calculate_score(results: dict) -> tuple[int, str]:
    """Calculate quality score and grade."""
    weights = {
        'structure': 25,
        'schema': 25,
        'components': 25,
        'quality': 25
    }

    score = sum(
        weights[gate] if passed else 0
        for gate, (passed, _) in results.items()
    )

    if score >= 90:
        grade = 'A'
    elif score >= 80:
        grade = 'B'
    elif score >= 70:
        grade = 'C'
    elif score >= 60:
        grade = 'D'
    else:
        grade = 'F'

    return score, grade

def main():
    plugin_root = get_plugin_root()

    # Run all gates
    results = {
        'structure': check_structure(plugin_root),
        'schema': check_schema(plugin_root),
        'components': check_components(plugin_root),
        'quality': check_quality(plugin_root)
    }

    # Calculate score
    score, grade = calculate_score(results)

    # Build report
    all_errors = []
    for gate, (passed, errors) in results.items():
        if errors:
            all_errors.extend([f"[{gate}] {e}" for e in errors])

    report = {
        "plugin": plugin_root.name,
        "score": score,
        "grade": grade,
        "gates": {
            gate: {"passed": passed, "errors": errors}
            for gate, (passed, errors) in results.items()
        },
        "summary": f"Quality Score: {score}/100 (Grade: {grade})"
    }

    print(json.dumps(report, indent=2))

    # Exit with appropriate code
    critical_failures = not results['structure'][0] or not results['schema'][0]
    if critical_failures:
        print("\nCritical validation failures detected.", file=sys.stderr)
        sys.exit(2)

    sys.exit(0)

if __name__ == '__main__':
    main()
