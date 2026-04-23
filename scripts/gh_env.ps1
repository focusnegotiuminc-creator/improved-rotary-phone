param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$GhArgs
)

$root = Split-Path -Parent $PSScriptRoot
$envFile = Join-Path $root '.secrets\focus_master.env'
$ghPath = 'C:\Users\reggi\OneDrive\Documents\GitHub\tools\gh\bin\gh.exe'
$bootstrap = Join-Path $PSScriptRoot 'bootstrap_gh_auth.ps1'
$configDir = Join-Path $env:APPDATA 'GitHub CLI'
$hostsPath = Join-Path $configDir 'hosts.yml'

if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^\s*#' -or $_ -notmatch '=') {
            return
        }
        $key, $value = $_ -split '=', 2
        $trimmed = $value.Trim().Trim('"')
        if ($key -eq 'GITHUB_TOKEN' -and -not $env:GH_TOKEN) {
            $env:GH_TOKEN = $trimmed
        }
        if ($key -eq 'GH_TOKEN') {
            $env:GH_TOKEN = $trimmed
        }
    }
}

if (-not $env:GH_TOKEN) {
    throw 'GH_TOKEN is not set. Update .secrets\focus_master.env first.'
}

if (-not (Test-Path $hostsPath) -and (Test-Path $bootstrap)) {
    & $bootstrap -Quiet
}

& $ghPath @GhArgs
