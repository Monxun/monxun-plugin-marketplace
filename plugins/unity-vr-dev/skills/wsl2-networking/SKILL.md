---
name: wsl2-networking
description: |
  WSL2 networking configuration for Unity VR development on Windows.
  Use when: WSL2 networking, mirrored mode, NAT port forwarding,
  Docker networking, Windows firewall, localhost access from WSL,
  "WSL2 setup", "port forwarding", "can't connect from WSL".
  Supports: mirrored mode, NAT mode, Docker Desktop integration.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# WSL2 Networking

Configure WSL2 networking for Unity VR development environments on Windows.

## Architecture

Unity Editor runs on Windows. Docker services (if any) run in WSL2. The Quest connects via ADB to the Windows host. MCP communication flows:

```
Quest ← ADB → Windows Host ← MCP HTTP → Unity Editor
                 ↕
              WSL2/Docker (services, build tools)
```

## Networking Modes

### Mirrored Mode (Recommended)

**Requirements**: Windows 11 22H2+, WSL 2.0.4+, Docker Desktop 4.26.0+

WSL2 shares the Windows host network. Services in WSL2 are accessible on `localhost` from Windows and vice versa.

#### Configuration

Create or edit `%USERPROFILE%/.wslconfig`:

```ini
[wsl2]
networkingMode=mirrored
```

Then restart WSL:
```bash
wsl --shutdown
```

#### Verification

```bash
# From WSL2, access Windows localhost
curl http://localhost:8080/health  # Should reach Unity MCP server

# From Windows, access WSL2 services
curl http://localhost:3000  # Should reach WSL2 services
```

See `references/mirrored-mode.md` for advanced mirrored mode configuration.

### NAT Mode (Legacy)

Default WSL2 networking. WSL2 has its own IP address. Port forwarding required to access services across the boundary.

#### Port Forwarding

```powershell
# Forward port from Windows to WSL2
netsh interface portproxy add v4tov4 `
  listenport=8080 listenaddress=0.0.0.0 `
  connectport=8080 connectaddress=$(wsl hostname -I)
```

**Note**: WSL2 IP changes on restart. Use dynamic IP retrieval:

```powershell
$wslIp = (wsl hostname -I).Trim()
netsh interface portproxy add v4tov4 `
  listenport=8080 listenaddress=0.0.0.0 `
  connectport=8080 connectaddress=$wslIp
```

#### Windows Firewall

```powershell
# Allow inbound on forwarded port
New-NetFirewallRule -DisplayName "WSL2 MCP" `
  -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
```

See `references/port-forwarding.md` for NAT mode automation scripts.

## Docker Desktop Integration

### With Mirrored Mode

Docker Desktop (4.26.0+) works with mirrored networking. Containers bind to localhost and are directly accessible from Windows.

```yaml
# docker-compose.yml
services:
  mcp-service:
    ports:
      - "8080:8080"  # Accessible on localhost from Windows
```

### With NAT Mode

Requires port forwarding for each exposed container port.

## Common Scenarios

### Unity MCP from WSL2

If running tools or scripts in WSL2 that need to reach the Unity MCP server on Windows:

**Mirrored mode**: Just use `localhost:8080`

**NAT mode**: Use the Windows host IP:
```bash
# Get Windows host IP from WSL2
HOST_IP=$(ip route show | grep -i default | awk '{ print $3}')
curl http://$HOST_IP:8080/health
```

### ADB from WSL2

ADB in WSL2 needs to connect to USB devices on Windows:

```bash
# Option 1: Use ADB on Windows via interop
/mnt/c/Users/<user>/AppData/Local/Android/Sdk/platform-tools/adb.exe devices

# Option 2: USB/IP passthrough (usbipd)
# On Windows (PowerShell admin):
usbipd list
usbipd bind --busid <busid>
usbipd attach --wsl --busid <busid>
```

## Troubleshooting

| Issue | Mode | Fix |
|-------|------|-----|
| Can't reach Windows from WSL2 | NAT | Use host IP from `ip route` |
| Can't reach WSL2 from Windows | NAT | Add port forwarding rule |
| Port forwarding stops working | NAT | WSL2 IP changed; re-run script |
| Docker ports not accessible | NAT | Forward each container port |
| Everything works | Mirrored | Correct configuration |

## References

- `references/mirrored-mode.md` — Mirrored mode setup and configuration
- `references/port-forwarding.md` — NAT mode port forwarding automation
