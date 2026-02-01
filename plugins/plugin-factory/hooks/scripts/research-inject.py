#!/usr/bin/env python3
"""
SessionStart hook: Inject research context at session start.

This hook provides Claude with latest patterns and best practices
when a plugin-factory session begins.
"""

import json
import sys
import os
from pathlib import Path

def get_plugin_root() -> Path:
    """Get plugin root directory."""
    return Path(os.environ.get('CLAUDE_PLUGIN_ROOT', Path(__file__).parent.parent.parent))

def load_heuristics() -> dict:
    """Load quality heuristics from skills."""
    plugin_root = get_plugin_root()
    heuristics_skill = plugin_root / 'skills' / 'heuristics-engine' / 'SKILL.md'

    if heuristics_skill.exists():
        with open(heuristics_skill, 'r') as f:
            content = f.read()
        return {
            "quality_gates": extract_section(content, "Quality Gates"),
            "anti_patterns": extract_section(content, "Anti-Patterns")
        }
    return {}

def extract_section(content: str, section_name: str) -> str:
    """Extract a markdown section."""
    import re
    pattern = rf'## {section_name}\n(.*?)(?=\n## |\Z)'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else ""

def get_context() -> dict:
    """Build research context for injection."""
    return {
        "plugin_factory_version": "1.0.0",
        "heuristics": load_heuristics(),
        "reminders": [
            "Use kebab-case for all names",
            "SKILL.md must be < 500 lines",
            "Include trigger keywords in descriptions",
            "Only plugin.json in .claude-plugin/",
            "Components at plugin root level",
            "Exit code 2 blocks operations"
        ],
        "validation_loop": {
            "max_iterations": 5,
            "gates": ["structure", "schema", "components", "quality", "integration"]
        }
    }

def main():
    """Output research context for Claude."""
    context = get_context()

    # Output as JSON for Claude to parse
    output = {
        "type": "research_context",
        "data": context,
        "message": "Plugin Factory research context loaded. Quality heuristics active."
    }

    print(json.dumps(output, indent=2))
    sys.exit(0)

if __name__ == '__main__':
    main()
