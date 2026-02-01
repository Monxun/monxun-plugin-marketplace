---
name: cli-integration
description: Manage flutter-deploy CLI tool integration. Check installation, install CLI, run CLI commands, and parse output for agent workflows. Use when managing CLI tools or integrating CLI output.
trigger_keywords:
  - cli
  - flutter-deploy
  - install cli
  - cli status
  - run cli
  - cli tool
---

# Flutter Deploy CLI Integration

Manage the flutter-deploy CLI tool for enhanced deployment automation.

## Quick Check

```bash
# Check if CLI is available
which flutter-deploy || echo "Not installed"

# Get version
flutter-deploy --version 2>/dev/null || echo "CLI not available"
```

## Installation

The CLI is bundled with this plugin in `scripts/flutter-deploy-cli/`.

```bash
# Install from bundled source
pip install -e scripts/flutter-deploy-cli/ --user

# Verify installation
flutter-deploy --version
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `flutter-deploy` | Launch interactive mode |
| `fd` | Short alias for flutter-deploy |

## Using CLI in Workflows

### Check CLI Availability

```python
import subprocess

def cli_available():
    try:
        result = subprocess.run(
            ["flutter-deploy", "--version"],
            capture_output=True, timeout=5
        )
        return result.returncode == 0
    except:
        return False
```

### Run Analysis

```bash
# Navigate to Flutter project
cd /path/to/flutter-project

# Run analysis phase
flutter-deploy  # Select "Analyze Flutter App"
```

### Parse CLI Output

CLI stores configuration in `flutter-deploy-config.json`:

```json
{
  "project_name": "my_app",
  "ios_bundle_id": "com.example.myapp",
  "android_package_name": "com.example.myapp",
  "firebase": {
    "enabled": true,
    "services": ["auth", "firestore"]
  }
}
```

## Agent Integration Pattern

When CLI is available, prefer CLI for:
- Interactive configuration (phases 1-5)
- User-driven setup wizards

When CLI unavailable, fall back to:
- Agent-based file analysis
- Programmatic configuration generation

## Fallback Strategy

```
1. Check CLI installed → Yes → Use CLI
                       → No  → Continue with agent-only
2. Run CLI phase → Success → Use CLI output
                 → Failure → Fall back to agent
3. Merge results from both when applicable
```

## References

See bundled CLI documentation at `scripts/flutter-deploy-cli/README.md`.
