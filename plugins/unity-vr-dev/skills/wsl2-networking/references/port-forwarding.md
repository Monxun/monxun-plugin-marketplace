# WSL2 NAT Mode Port Forwarding

## Overview

In NAT mode, WSL2 has its own IP address on a virtual network. Port forwarding bridges Windows and WSL2 network namespaces.

## Manual Port Forwarding

### Add Forward Rule

```powershell
# Get WSL2 IP
$wslIp = (wsl hostname -I).Trim()

# Forward port
netsh interface portproxy add v4tov4 `
  listenport=8080 `
  listenaddress=0.0.0.0 `
  connectport=8080 `
  connectaddress=$wslIp
```

### List Active Rules

```powershell
netsh interface portproxy show all
```

### Remove Forward Rule

```powershell
netsh interface portproxy delete v4tov4 `
  listenport=8080 `
  listenaddress=0.0.0.0
```

### Remove All Rules

```powershell
netsh interface portproxy reset
```

## Windows Firewall

Port forwarding requires firewall rules for inbound traffic:

```powershell
# Allow specific port
New-NetFirewallRule `
  -DisplayName "WSL2 Port 8080" `
  -Direction Inbound `
  -LocalPort 8080 `
  -Protocol TCP `
  -Action Allow

# Allow port range
New-NetFirewallRule `
  -DisplayName "WSL2 Dev Ports" `
  -Direction Inbound `
  -LocalPort 8080-8090 `
  -Protocol TCP `
  -Action Allow
```

### Remove Firewall Rule

```powershell
Remove-NetFirewallRule -DisplayName "WSL2 Port 8080"
```

## Automation Script

Since WSL2 IP changes on restart, automate port forwarding:

### PowerShell Script

```powershell
# setup-wsl-forwarding.ps1
# Run as Administrator

param(
    [int[]]$Ports = @(8080, 3000, 5000)
)

$wslIp = (wsl hostname -I).Trim()
Write-Host "WSL2 IP: $wslIp"

foreach ($port in $Ports) {
    # Remove existing rule
    netsh interface portproxy delete v4tov4 `
        listenport=$port listenaddress=0.0.0.0 2>$null

    # Add new rule
    netsh interface portproxy add v4tov4 `
        listenport=$port `
        listenaddress=0.0.0.0 `
        connectport=$port `
        connectaddress=$wslIp

    Write-Host "Forwarded port $port -> ${wslIp}:${port}"

    # Ensure firewall rule exists
    $ruleName = "WSL2 Port $port"
    $existing = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
    if (-not $existing) {
        New-NetFirewallRule `
            -DisplayName $ruleName `
            -Direction Inbound `
            -LocalPort $port `
            -Protocol TCP `
            -Action Allow | Out-Null
        Write-Host "Created firewall rule: $ruleName"
    }
}

Write-Host "`nActive port forwards:"
netsh interface portproxy show all
```

### Run at Startup

Create a scheduled task to run on WSL start:

```powershell
# Create scheduled task (run as admin)
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -File C:\Scripts\setup-wsl-forwarding.ps1"

$trigger = New-ScheduledTaskTrigger -AtLogon

Register-ScheduledTask `
    -TaskName "WSL2 Port Forwarding" `
    -Action $action `
    -Trigger $trigger `
    -RunLevel Highest
```

## Accessing Windows from WSL2

To reach Windows services from inside WSL2:

```bash
# Get Windows host IP
HOST_IP=$(ip route show | grep -i default | awk '{ print $3}')

# Access Unity MCP server on Windows
curl http://$HOST_IP:8080/health

# Or use /etc/resolv.conf nameserver (same as host IP)
HOST_IP=$(cat /etc/resolv.conf | grep nameserver | awk '{ print $2}')
```

## Common Ports for VR Development

| Port | Service | Direction |
|------|---------|-----------|
| 8080 | Unity MCP Server | WSL2 → Windows |
| 5555 | ADB Wireless | Windows → Quest |
| 3000 | Dev server | WSL2 → Windows |
| 5037 | ADB Server | Both |

## Troubleshooting

### Port Forward Not Working

```powershell
# Verify WSL2 is running
wsl --list --verbose

# Verify WSL2 IP is reachable
ping $(wsl hostname -I)

# Check port is listening in WSL2
wsl ss -tlnp | grep 8080

# Check Windows port forwarding
netsh interface portproxy show all
```

### IP Changed After Restart

Re-run the automation script. The WSL2 IP changes every time WSL restarts.

### Connection Refused

1. Verify the service is running in WSL2
2. Verify the service binds to `0.0.0.0` (not just `127.0.0.1`)
3. Check Windows Firewall rules
4. Check port forwarding target IP matches current WSL2 IP
