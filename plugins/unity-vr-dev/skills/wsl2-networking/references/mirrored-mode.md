# WSL2 Mirrored Networking Mode

## Requirements

- Windows 11 22H2 or later
- WSL 2.0.4 or later
- Docker Desktop 4.26.0 or later (if using Docker)

## Configuration

### .wslconfig

Location: `%USERPROFILE%/.wslconfig` (e.g., `C:\Users\YourName\.wslconfig`)

```ini
[wsl2]
networkingMode=mirrored

# Optional: DNS tunneling for better DNS resolution
dnsTunneling=true

# Optional: auto-proxy for corporate networks
autoProxy=true
```

### Apply Changes

```powershell
# Restart WSL to apply
wsl --shutdown
wsl
```

### Verify

```bash
# From WSL2
ip addr show eth0
# Should show same subnet as Windows host

# Test connectivity to Windows services
curl -s http://localhost:8080/health
```

## How It Works

In mirrored mode, WSL2 shares the Windows host's network interfaces. This means:

- WSL2 services bind to the same `localhost` as Windows
- No port forwarding needed
- No separate IP address for WSL2
- Docker containers are directly accessible on `localhost`

## Benefits Over NAT Mode

| Feature | Mirrored | NAT |
|---------|----------|-----|
| localhost sharing | Yes | No |
| Port forwarding | Not needed | Required |
| IP stability | Same as host | Changes on restart |
| Docker access | Direct | Forwarding needed |
| Setup complexity | Minimal | Moderate |

## Limitations

- Requires Windows 11 22H2+ (not available on Windows 10)
- Some VPN software may conflict with mirrored networking
- Listening on `0.0.0.0` in WSL2 exposes to all host interfaces
- IPv6 behavior may differ from NAT mode

## VPN Compatibility

If using a VPN that causes issues with mirrored mode:

```ini
[wsl2]
networkingMode=mirrored

# Exclude VPN interfaces
networkingMode.excludedInterfaces={"name": "VPN Interface Name"}
```

## Docker Desktop Configuration

Ensure Docker Desktop is configured for WSL2 backend:

1. Docker Desktop > Settings > General > Use WSL 2 based engine: ✓
2. Settings > Resources > WSL Integration > Enable for your distro
3. Restart Docker Desktop after changing `.wslconfig`

### Verify Docker Networking

```bash
# From WSL2
docker run --rm -p 8081:80 nginx
# From Windows browser: http://localhost:8081 should show nginx
```

## Firewall Notes

With mirrored mode, Windows Firewall rules apply to WSL2 traffic. If a service in WSL2 is blocked:

```powershell
# Allow specific port
New-NetFirewallRule -DisplayName "WSL2 Service" `
  -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
```

## Rollback to NAT Mode

If mirrored mode causes issues:

```ini
[wsl2]
# Comment out or remove networkingMode
# networkingMode=mirrored
```

```powershell
wsl --shutdown
wsl
```
