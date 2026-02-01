#!/usr/bin/env python3
"""
Session initialization hook for RLM plugin.
Sets up the session environment and loads any persisted contexts.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime


def main():
    """Initialize RLM session."""
    try:
        # Read input from stdin (MCP provides JSON)
        input_data = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except json.JSONDecodeError:
        input_data = {}
    
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", ".")
    data_dir = Path(plugin_root) / "data"
    
    # Ensure data directory exists
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Find any persisted contexts
    persisted_contexts = list(data_dir.glob("*.json"))
    
    # Prepare session info
    session_info = {
        "initialized_at": datetime.now().isoformat(),
        "data_dir": str(data_dir),
        "persisted_contexts": len(persisted_contexts),
        "config": {
            "max_depth": int(os.environ.get("RLM_MAX_DEPTH", "10")),
            "chunk_size": int(os.environ.get("RLM_CHUNK_SIZE", "4000")),
            "overlap": int(os.environ.get("RLM_OVERLAP", "200"))
        }
    }
    
    # Log to stderr (not stdout - MCP requirement)
    print(f"RLM Session initialized: {session_info['initialized_at']}", file=sys.stderr)
    print(f"Found {len(persisted_contexts)} persisted contexts", file=sys.stderr)
    
    # Output session info as JSON
    output = {
        "session_initialized": True,
        "context": session_info
    }
    
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
