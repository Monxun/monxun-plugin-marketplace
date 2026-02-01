#!/usr/bin/env python3
"""Pre-deploy hook: Verify ADB device is connected before deployment commands.

Exit codes:
  0 - ADB device connected or command is not a deployment command
  2 - Block: deployment command detected but no ADB device connected
  1 - Non-blocking error (ADB not found, etc.)
"""

import json
import os
import subprocess
import sys


def get_tool_input():
    """Read tool input from CLAUDE_TOOL_INPUT environment variable."""
    tool_input = os.environ.get("CLAUDE_TOOL_INPUT", "{}")
    try:
        return json.loads(tool_input)
    except json.JSONDecodeError:
        return {}


def is_deployment_command(command: str) -> bool:
    """Check if the bash command involves ADB deployment."""
    deploy_keywords = [
        "adb install",
        "adb push",
        "adb shell am start",
        "adb shell pm",
        "deploy-to-device",
        "deploy-quest",
    ]
    command_lower = command.lower()
    return any(kw in command_lower for kw in deploy_keywords)


def check_adb_devices() -> bool:
    """Check if at least one ADB device is connected."""
    try:
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        lines = result.stdout.strip().split("\n")
        # Filter out header and empty lines
        devices = [
            line for line in lines[1:] if line.strip() and "device" in line
        ]
        return len(devices) > 0
    except FileNotFoundError:
        print("Warning: ADB not found in PATH", file=sys.stderr)
        return False
    except subprocess.TimeoutExpired:
        print("Warning: ADB command timed out", file=sys.stderr)
        return False


def main():
    tool_input = get_tool_input()
    command = tool_input.get("command", "")

    # Only check for deployment commands
    if not is_deployment_command(command):
        sys.exit(0)

    # Check ADB connection
    if check_adb_devices():
        sys.exit(0)
    else:
        print(
            "BLOCKED: No ADB device connected. "
            "Connect a Quest device via USB or wireless ADB before deploying.\n"
            "  USB: Connect cable and authorize on headset\n"
            "  Wireless: adb tcpip 5555 && adb connect <device-ip>:5555",
            file=sys.stderr,
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
