# Gradle Caching for Quest Builds

## Cache Configuration

### Enable Build Cache

In the exported Gradle project's `gradle.properties`:

```properties
# Build caching
org.gradle.caching=true
android.enableBuildCache=true

# Parallel execution
org.gradle.parallel=true

# Daemon (keeps Gradle JVM running between builds)
org.gradle.daemon=true

# Memory allocation
org.gradle.jvmargs=-Xmx4096m -XX:+HeapDumpOnOutOfMemoryError

# R8 (code shrinking) cache
android.enableR8.fullMode=true
```

### Local Cache Directory

```properties
# Custom cache location (gradle.properties)
org.gradle.caching=true

# Or in init.gradle
buildCache {
    local {
        directory = new File(rootDir, '.gradle-cache')
        removeUnusedEntriesAfterDays = 30
    }
}
```

### Cache Location

Default: `~/.gradle/caches/`

```bash
# Check cache size
du -sh ~/.gradle/caches/

# Clear stale caches
rm -rf ~/.gradle/caches/build-cache-*
rm -rf ~/.gradle/caches/transforms-*
```

## Incremental Build Strategy

### What Gets Cached

| Component | Cached? | Notes |
|-----------|---------|-------|
| IL2CPP C++ output | Yes | `Library/Il2cppBuildCache/` |
| Gradle compilation | Yes | `.gradle/` in project |
| DEX conversion | Yes | Gradle build cache |
| APK packaging | Partial | Resources may re-pack |
| Asset processing | Yes | `Library/` folder |

### Typical Speed Improvements

| Build Type | Clean Build | Cached Build | Improvement |
|-----------|-------------|-------------|-------------|
| Code-only change | 5-10 min | 2-5 min | 30-50% |
| Asset change | 5-10 min | 3-6 min | 20-40% |
| Config change | 5-10 min | 4-8 min | 10-30% |
| Full clean | 8-15 min | N/A | Baseline |

### Maximizing Cache Hits

1. **Don't clean between builds** — Let IL2CPP and Gradle reuse cached outputs
2. **Use consistent build settings** — Changing options invalidates caches
3. **Keep Library/ intact** — Contains IL2CPP build cache
4. **Same output path** — Changing APK output path may invalidate packaging cache

## CI/CD Cache Strategy

### GitHub Actions Cache

```yaml
- name: Cache Gradle
  uses: actions/cache@v3
  with:
    path: |
      ~/.gradle/caches
      ~/.gradle/wrapper
    key: gradle-${{ hashFiles('**/*.gradle*') }}
    restore-keys: gradle-

- name: Cache IL2CPP
  uses: actions/cache@v3
  with:
    path: Library/Il2cppBuildCache
    key: il2cpp-${{ hashFiles('Assets/**/*.cs') }}
    restore-keys: il2cpp-
```

### Cache Invalidation

Caches should be invalidated when:
- Unity version changes
- Android SDK/NDK version changes
- Gradle plugin version changes
- Significant dependency changes

```bash
# Force clean build
rm -rf Library/Il2cppBuildCache/
rm -rf Temp/gradleOut/
```

## Troubleshooting

### Build Fails After Cache

**Symptom**: Build errors that don't occur on clean build

**Fix**: Incremental delete of specific caches:
```bash
# Try in order, rebuilding after each:
rm -rf Temp/gradleOut/
rm -rf Library/Il2cppBuildCache/
rm -rf Library/Bee/
```

### Gradle Daemon Memory Issues

**Symptom**: `OutOfMemoryError` during build

**Fix**: Increase daemon memory:
```properties
org.gradle.jvmargs=-Xmx6144m -XX:MaxMetaspaceSize=512m
```

### Cache Size Growing

**Symptom**: Disk usage steadily increasing

**Fix**: Configure cache eviction:
```groovy
buildCache {
    local {
        removeUnusedEntriesAfterDays = 14
    }
}
```
