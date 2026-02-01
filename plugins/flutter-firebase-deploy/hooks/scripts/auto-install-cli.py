#!/usr/bin/env python3
"""Auto-install flutter-deploy CLI if not present.

This hook runs on SessionStart to ensure the flutter-deploy CLI is available.
Installation is silent - no user prompts, no blocking on failure.
"""

import subprocess
import sys
import os
from pathlib import Path


def get_python_version():
    """Get current Python version as tuple."""
    return sys.version_info[:2]


def check_cli_installed():
    """Check if flutter-deploy CLI is callable."""
    try:
        result = subprocess.run(
            ["flutter-deploy", "--version"], capture_output=True, timeout=5
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False
    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False


def get_cli_version():
    """Get installed CLI version if available."""
    try:
        result = subprocess.run(
            ["flutter-deploy", "--version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def install_cli():
    """Install CLI from bundled source.

    Returns True if installation succeeded, False otherwise.
    """
    # Get plugin root from environment or derive from script location
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT")

    if not plugin_root:
        # Derive from script location: hooks/scripts/auto-install-cli.py
        script_path = Path(__file__).resolve()
        plugin_root = script_path.parent.parent.parent
    else:
        plugin_root = Path(plugin_root)

    cli_path = plugin_root / "scripts" / "flutter-deploy-cli"

    if not cli_path.exists():
        # CLI source not bundled, cannot install
        return False

    # Check Python version (require 3.10+)
    py_version = get_python_version()
    if py_version < (3, 10):
        # Python too old, skip silently
        return False

    try:
        # Install in editable mode, quietly
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-e",
                str(cli_path),
                "-q",
                "--user",
            ],
            capture_output=True,
            timeout=120,  # 2 minute timeout for pip install
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False


def main():
    """Main hook entry point.

    Always exits with 0 (continue) - installation is best-effort.
    Prints status to stderr for logging but doesn't block.
    """
    if check_cli_installed():
        version = get_cli_version()
        if version:
            print(f"flutter-deploy CLI ready: {version}", file=sys.stderr)
        sys.exit(0)

    # Not installed, try to install
    print("flutter-deploy CLI not found, installing...", file=sys.stderr)

    if install_cli():
        # Verify installation
        if check_cli_installed():
            version = get_cli_version()
            print(f"flutter-deploy CLI installed: {version}", file=sys.stderr)
        else:
            print("flutter-deploy CLI installed but not in PATH", file=sys.stderr)
    else:
        print(
            "flutter-deploy CLI installation skipped (will use agent-only mode)",
            file=sys.stderr,
        )

    # Always continue regardless of installation result
    sys.exit(0)


if __name__ == "__main__":
    main()
