#!/usr/bin/env python3
"""
Session summary hook for RLM plugin.
Generates summary of RLM usage when session ends.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime


def load_usage_log(log_file: Path) -> list:
    """Load usage log entries."""
    if not log_file.exists():
        return []
    
    entries = []
    try:
        with open(log_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except Exception:
        pass
    
    return entries


def generate_summary(entries: list) -> dict:
    """Generate session summary from usage entries."""
    if not entries:
        return {
            "total_searches": 0,
            "message": "No RLM searches performed this session."
        }
    
    total_searches = len(entries)
    total_tokens = sum(e.get("tokens", 0) for e in entries)
    total_results = sum(e.get("results", 0) for e in entries)
    max_depth = max((e.get("depth", 0) for e in entries), default=0)
    
    # Search type breakdown
    search_types = {}
    for e in entries:
        st = e.get("search_type", "unknown")
        search_types[st] = search_types.get(st, 0) + 1
    
    # Queries list
    queries = [e.get("query", "") for e in entries if e.get("query")]
    
    return {
        "total_searches": total_searches,
        "total_tokens_processed": total_tokens,
        "total_results_returned": total_results,
        "max_recursion_depth": max_depth,
        "search_type_breakdown": search_types,
        "unique_queries": len(set(queries)),
        "avg_tokens_per_search": total_tokens // total_searches if total_searches > 0 else 0,
        "avg_results_per_search": total_results / total_searches if total_searches > 0 else 0
    }


def main():
    """Generate RLM session summary."""
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        input_data = {}
    
    # Check if stop hook already active (prevent loops)
    if input_data.get("stop_hook_active", False):
        sys.exit(0)
    
    # Load usage log
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", ".")
    log_file = Path(plugin_root) / "data" / "usage.log"
    
    entries = load_usage_log(log_file)
    summary = generate_summary(entries)
    
    # Log summary
    print(f"\n=== RLM Session Summary ===", file=sys.stderr)
    print(f"Total searches: {summary['total_searches']}", file=sys.stderr)
    print(f"Tokens processed: {summary.get('total_tokens_processed', 0):,}", file=sys.stderr)
    print(f"Max depth: {summary.get('max_recursion_depth', 0)}", file=sys.stderr)
    print(f"===========================\n", file=sys.stderr)
    
    # Clear usage log for next session
    try:
        if log_file.exists():
            # Archive instead of delete
            archive_file = log_file.with_suffix(f'.log.{datetime.now().strftime("%Y%m%d_%H%M%S")}')
            log_file.rename(archive_file)
    except Exception:
        pass
    
    # Output summary
    output = {
        "session_summary": summary,
        "ended_at": datetime.now().isoformat()
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
