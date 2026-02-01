# LogCat Filtering Guide

## Tag-Based Filtering

### Unity-Specific Tags

```bash
# Core Unity tags
adb logcat -s Unity         # Unity engine logs
adb logcat -s UnityMain     # Main thread logs

# VR-specific tags
adb logcat -s VrApi                  # Meta VR runtime
adb logcat -s XrPerformanceManager   # XR performance metrics
adb logcat -s OVRPlugin              # OVR plugin events

# Android system tags
adb logcat -s ActivityManager   # Activity lifecycle
adb logcat -s PackageManager    # Package install/update
adb logcat -s dalvikvm          # VM events
adb logcat -s DEBUG             # Native crashes
```

### Combined Tag Filter

```bash
# Full VR debug filter
adb logcat -s Unity,VrApi,XrPerformanceManager,ActivityManager,PackageManager,dalvikvm,DEBUG

# Performance focus
adb logcat -s VrApi,XrPerformanceManager,OVRPlugin

# Crash investigation
adb logcat -s DEBUG,Unity:E,dalvikvm:E
```

## Severity Filtering

```bash
# Only errors and fatals from all tags
adb logcat *:E

# Warnings and above from Unity, errors from VrApi
adb logcat -s Unity:W VrApi:E

# Verbose output for specific tag
adb logcat -s Unity:V
```

## Regex Filtering

```bash
# Filter by message content
adb logcat -s Unity | grep -i "exception"
adb logcat -s Unity | grep -i "error\|warning\|null"
adb logcat -s Unity | grep -E "FPS|frame|render"

# Exclude noise
adb logcat -s Unity | grep -v "GarbageCollector\|Shader\|Loading"

# Performance metrics extraction
adb logcat -s VrApi | grep -E "FPS=[0-9]+"
```

## Output Formatting

```bash
# With timestamps
adb logcat -v time -s Unity

# With thread info
adb logcat -v threadtime -s Unity

# With process info
adb logcat -v process -s Unity

# Brief format (tag and message only)
adb logcat -v brief -s Unity
```

## Log Capture to File

```bash
# Capture to file
adb logcat -s Unity > unity_logs.txt

# Capture with timeout (30 seconds)
timeout 30 adb logcat -s Unity > unity_logs.txt

# Append to existing file
adb logcat -s Unity >> unity_logs.txt
```

## Common Log Patterns

### Null Reference

```
E Unity   : NullReferenceException: Object reference not set to an instance of an object
```

Filter: `adb logcat -s Unity:E | grep "NullReference"`

### Memory Warnings

```
W Unity   : [GarbageCollector] GC.Alloc exceeded threshold
```

Filter: `adb logcat -s Unity:W | grep "GarbageCollector\|memory\|alloc"`

### XR Performance Drops

```
W VrApi   : FPS=72 Prd=0 Tear=0 Early=0 Stale=18
```

Filter: `adb logcat -s VrApi | grep "Stale=[1-9]"`

### Native Crashes

```
F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR)
```

Filter: `adb logcat -s DEBUG | grep "signal\|backtrace\|SEGV"`

## Session Management

```bash
# Clear all logs before starting
adb logcat -c

# Get log buffer size
adb logcat -g

# Dump current log and exit
adb logcat -d -s Unity

# Ring buffer (last N lines)
adb logcat -t 100 -s Unity
```
