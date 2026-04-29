$ErrorActionPreference = "Stop"

$workspace = "G:\My Drive\FOCUS_MASTER_AI_live"
$python = "python"
$tailscale = "C:\Program Files\Tailscale\tailscale.exe"
$healthUrl = "http://127.0.0.1:8000/health"
$tailnetUrl = "https://msi.tail894763.ts.net/health"

function Test-Health {
    param([string]$Url)
    try {
        $response = Invoke-WebRequest -UseBasicParsing -Uri $Url -TimeoutSec 10
        return $response.StatusCode -eq 200
    } catch {
        return $false
    }
}

if (-not (Test-Health -Url $healthUrl)) {
    $command = "Set-Location '$workspace'; " +
        "$env:FOCUS_API_HOST='127.0.0.1'; " +
        "$env:FOCUS_API_PORT='8000'; " +
        "python -c ""from FOCUS_MASTER_AI.api_server import app; app.run(host='127.0.0.1', port=8000, debug=False)"""
    Start-Process -FilePath powershell.exe -ArgumentList "-NoProfile", "-Command", $command -WindowStyle Hidden
    Start-Sleep -Seconds 4
}

& $tailscale funnel reset | Out-Null
& $tailscale serve --bg http://127.0.0.1:8000 | Out-Null
& $tailscale set --accept-routes=false --unattended=true | Out-Null

$localOk = Test-Health -Url $healthUrl
$tailnetOk = Test-Health -Url $tailnetUrl

Write-Output ("LOCAL_HEALTH=" + $localOk)
Write-Output ("TAILNET_HEALTH=" + $tailnetOk)
Write-Output "TAILNET_URL=https://msi.tail894763.ts.net/private-console"
