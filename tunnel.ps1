# ConnectLAW - lokales Backend + HTTPS-Tunnel (cloudflared) fuer Windows.
#
# Start in PowerShell (im Projektordner):
#   powershell -ExecutionPolicy Bypass -File .\tunnel.ps1
#
# Voraussetzungen:
#   - Python + "pip install -r requirements-server.txt"
#   - cloudflared installiert  (winget install --id Cloudflare.cloudflared)
#   - .env mit ANTHROPIC_API_KEY

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# .env laden (einfaches KEY=VALUE-Format)
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match '^\s*([^#=][^=]*)=(.*)$') {
            $name = $matches[1].Trim()
            $val  = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($name, $val, "Process")
        }
    }
}

if (-not $env:ANTHROPIC_API_KEY) {
    Write-Error "ANTHROPIC_API_KEY nicht gesetzt. Bitte in .env eintragen."
    exit 1
}

if (-not (Get-Command cloudflared -ErrorAction SilentlyContinue)) {
    Write-Error "'cloudflared' nicht gefunden. Installieren: winget install --id Cloudflare.cloudflared"
    exit 1
}

if (-not $env:CONNECTLAW_CORS_ORIGINS) {
    $env:CONNECTLAW_CORS_ORIGINS = "https://acortese-wq.github.io"
}
$port = if ($env:PORT) { $env:PORT } else { "8000" }

Write-Host "Starte Backend auf http://localhost:$port (CORS: $($env:CONNECTLAW_CORS_ORIGINS)) ..."
$backend = Start-Process -PassThru -NoNewWindow uvicorn `
    -ArgumentList "server:app", "--host", "127.0.0.1", "--port", $port
Start-Sleep -Seconds 3

try {
    Write-Host ""
    Write-Host "Starte HTTPS-Tunnel. Die ausgegebene https-URL unten in der Chat-Seite"
    Write-Host "unter  Backend-Einstellungen  eintragen (ohne / am Ende, ohne /chat)."
    Write-Host "---------------------------------------------------------------"
    cloudflared tunnel --url "http://localhost:$port"
}
finally {
    if ($backend -and -not $backend.HasExited) {
        Write-Host ""
        Write-Host "Beende Backend ..."
        Stop-Process -Id $backend.Id -Force -ErrorAction SilentlyContinue
    }
}
