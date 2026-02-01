#!/usr/bin/env bash
# Post-build hook: Generate APK size and build duration metrics.
# Runs after Bash tool use to detect and report build outputs.
#
# Exit codes:
#   0 - Always (non-blocking informational hook)

set -euo pipefail

# Read tool input
TOOL_INPUT="${CLAUDE_TOOL_INPUT:-{}}"
COMMAND=$(echo "$TOOL_INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('command',''))" 2>/dev/null || echo "")

# Only process build-related commands
case "$COMMAND" in
  *buildplayer*|*build-quest*|*executeMethod*|*BuildPlayer*|*gradlew*|*"adb install"*)
    ;;
  *)
    exit 0
    ;;
esac

# Read tool output for build results
TOOL_OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

# Look for APK files in common build output locations
APK_PATHS=(
  "Builds/*.apk"
  "Build/*.apk"
  "build/*.apk"
  "*.apk"
)

FOUND_APK=""
for pattern in "${APK_PATHS[@]}"; do
  # shellcheck disable=SC2086
  for apk in $pattern; do
    if [ -f "$apk" ]; then
      FOUND_APK="$apk"
      break 2
    fi
  done
done

if [ -n "$FOUND_APK" ]; then
  # Get APK size
  APK_SIZE=$(du -sh "$FOUND_APK" | cut -f1)
  APK_SIZE_BYTES=$(stat -f%z "$FOUND_APK" 2>/dev/null || stat -c%s "$FOUND_APK" 2>/dev/null || echo "unknown")

  # Get modification time (proxy for build completion)
  MOD_TIME=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$FOUND_APK" 2>/dev/null || \
             stat -c "%y" "$FOUND_APK" 2>/dev/null | cut -d. -f1 || \
             echo "unknown")

  echo "=== Build Report ==="
  echo "APK: $FOUND_APK"
  echo "Size: $APK_SIZE ($APK_SIZE_BYTES bytes)"
  echo "Built: $MOD_TIME"
  echo "===================="
fi

exit 0
