param(
    [switch]$Quiet
)

$root = Split-Path -Parent $PSScriptRoot
$envFile = Join-Path $root '.secrets\focus_master.env'
$ghPath = 'C:\Users\reggi\OneDrive\Documents\GitHub\tools\gh\bin\gh.exe'
$configDir = Join-Path $env:APPDATA 'GitHub CLI'
$hostsPath = Join-Path $configDir 'hosts.yml'

if (-not (Test-Path $envFile)) {
    throw "Missing secrets file: $envFile"
}

$tokenLine = Get-Content $envFile | Where-Object { $_ -match '^(GH_TOKEN|GITHUB_TOKEN)=' } | Select-Object -First 1
if (-not $tokenLine) {
    throw 'No GH_TOKEN or GITHUB_TOKEN entry was found in focus_master.env.'
}

$token = ($tokenLine -split '=', 2)[1].Trim().Trim('"')
if (-not $token) {
    throw 'GitHub token entry is empty.'
}

$env:GH_TOKEN = $token
New-Item -ItemType Directory -Force -Path $configDir | Out-Null
@"
github.com:
    user: focusnegotiuminc-creator
    oauth_token: $token
    git_protocol: https
"@ | Set-Content -Path $hostsPath -Encoding utf8

& $ghPath auth setup-git | Out-Null
$status = & $ghPath auth status
$userJson = & $ghPath api user

if (-not $Quiet) {
    $status
    $userJson
}
