# Keystore Management for Quest Builds

## Creating a Keystore

### Command Line

```bash
keytool -genkey -v \
  -keystore quest-release.keystore \
  -alias quest-key \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -storepass "$KEYSTORE_PASS" \
  -keypass "$KEY_PASS" \
  -dname "CN=Developer,OU=VR,O=Company,L=City,ST=State,C=US"
```

### Unity GUI

1. Player Settings > Publishing Settings
2. Check "Custom Keystore"
3. Click "Create New Keystore..."
4. Set password and alias

## Security Best Practices

### Never Commit Keystores

```gitignore
# .gitignore
*.keystore
*.jks
keystore.properties
```

### Environment Variables

```bash
# Set in shell profile or CI secrets
export KEYSTORE_PATH="/secure/path/quest-release.keystore"
export KEYSTORE_PASS="secure-password"
export KEY_ALIAS="quest-key"
export KEY_PASS="secure-key-password"
```

### Unity Configuration via Script

```csharp
public static void ConfigureKeystore() {
    PlayerSettings.Android.useCustomKeystore = true;
    PlayerSettings.Android.keystoreName = Environment.GetEnvironmentVariable("KEYSTORE_PATH");
    PlayerSettings.Android.keystorePass = Environment.GetEnvironmentVariable("KEYSTORE_PASS");
    PlayerSettings.Android.keyaliasName = Environment.GetEnvironmentVariable("KEY_ALIAS");
    PlayerSettings.Android.keyaliasPass = Environment.GetEnvironmentVariable("KEY_PASS");
}
```

## CI/CD Integration

### GitHub Actions Secrets

```yaml
# In repository settings, add secrets:
# KEYSTORE_BASE64 - base64-encoded keystore file
# KEYSTORE_PASS
# KEY_ALIAS
# KEY_PASS

- name: Decode keystore
  run: echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 -d > quest-release.keystore

- name: Build with keystore
  env:
    KEYSTORE_PATH: quest-release.keystore
    KEYSTORE_PASS: ${{ secrets.KEYSTORE_PASS }}
    KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
    KEY_PASS: ${{ secrets.KEY_PASS }}
  run: unity-build-command
```

### Encode Keystore for CI

```bash
# Encode keystore as base64 for storage in CI secrets
base64 -i quest-release.keystore -o keystore-base64.txt
# Copy contents of keystore-base64.txt to CI secret
```

## Backup and Recovery

### Backup Strategy

1. Store keystore in secure location (password manager, hardware security module)
2. Keep encrypted backup separate from source code
3. Document the alias name and creation date
4. Test restoration periodically

### If Keystore is Lost

- Cannot update existing app on Meta Store
- Must submit as new application with new package name
- All existing installs become orphaned

**Prevention**: Always maintain at least 2 secure copies of production keystores.

## Debug vs Release Signing

### Debug Keystore

Unity auto-generates a debug keystore for development:
```
Location: ~/.android/debug.keystore
Alias: androiddebugkey
Password: android
```

Use debug keystore for:
- Local development builds
- Testing on personal devices
- CI development builds

### Release Keystore

Use custom keystore for:
- Meta App Lab submissions
- Meta Store releases
- Distribution builds

## Keystore Verification

```bash
# List keystore contents
keytool -list -v -keystore quest-release.keystore

# Verify APK signing
jarsigner -verify -verbose -certs Builds/QuestApp.apk

# Check APK signature (Android SDK)
apksigner verify --verbose Builds/QuestApp.apk
```
