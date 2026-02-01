#!/usr/bin/env python3
"""Pre-build hook: Validate Unity/XR SDK configuration before build commands.

Exit codes:
  0 - Not a build command, or validation passed
  2 - Block: critical build misconfiguration detected
  1 - Non-blocking warning
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


def is_build_command(command: str) -> bool:
    """Check if the bash command involves Unity builds."""
    build_keywords = [
        "buildplayer",
        "build-quest",
        "executemethod",
        "-batchmode",
        "buildpipeline",
        "build_quest",
        "gradlew",
    ]
    command_lower = command.lower()
    return any(kw in command_lower for kw in build_keywords)


def check_android_sdk() -> tuple[bool, str]:
    """Verify Android SDK is available."""
    android_home = os.environ.get("ANDROID_HOME") or os.environ.get(
        "ANDROID_SDK_ROOT"
    )
    if not android_home:
        return False, "ANDROID_HOME or ANDROID_SDK_ROOT not set"
    if not os.path.isdir(android_home):
        return False, f"Android SDK directory not found: {android_home}"
    return True, "OK"


def check_java() -> tuple[bool, str]:
    """Verify Java is available (required for Gradle builds)."""
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        # Java prints version to stderr
        version_output = result.stderr or result.stdout
        return True, version_output.split("\n")[0].strip()
    except FileNotFoundError:
        return False, "Java not found in PATH"
    except subprocess.TimeoutExpired:
        return False, "Java version check timed out"


def check_unity_project() -> tuple[bool, str]:
    """Check if we're in or near a Unity project."""
    # Look for ProjectSettings directory (marker of Unity project)
    search_dirs = [
        os.getcwd(),
        os.path.dirname(os.getcwd()),
    ]
    for d in search_dirs:
        if os.path.isdir(os.path.join(d, "ProjectSettings")):
            return True, d
    return False, "No Unity project found in current or parent directory"


def main():
    tool_input = get_tool_input()
    command = tool_input.get("command", "")

    # Only validate build commands
    if not is_build_command(command):
        sys.exit(0)

    warnings = []
    errors = []

    # Check Android SDK
    sdk_ok, sdk_msg = check_android_sdk()
    if not sdk_ok:
        warnings.append(f"Android SDK: {sdk_msg}")

    # Check Java
    java_ok, java_msg = check_java()
    if not java_ok:
        warnings.append(f"Java: {java_msg}")

    # Check Unity project
    project_ok, project_msg = check_unity_project()
    if not project_ok:
        errors.append(f"Unity project: {project_msg}")

    # Report results
    if errors:
        print(
            "BLOCKED: Build configuration errors:\n"
            + "\n".join(f"  - {e}" for e in errors),
            file=sys.stderr,
        )
        sys.exit(2)

    if warnings:
        print(
            "Build warnings (non-blocking):\n"
            + "\n".join(f"  - {w}" for w in warnings),
            file=sys.stderr,
        )
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
