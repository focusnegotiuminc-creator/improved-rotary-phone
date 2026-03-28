$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$workspaceRoot = Split-Path -Parent $repoRoot
$desktopRoot = [Environment]::GetFolderPath("Desktop")
$stamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$archiveDir = Join-Path $desktopRoot "Focus-AI-Archive"
$archivePath = Join-Path $archiveDir ("Focus-AI-archive-" + $stamp + ".zip")

New-Item -ItemType Directory -Force -Path $archiveDir | Out-Null

$stagingDir = Join-Path $archiveDir ("staging-" + $stamp)
New-Item -ItemType Directory -Force -Path $stagingDir | Out-Null

Copy-Item -Recurse -Force $workspaceRoot (Join-Path $stagingDir "Focus--Master")
if (Test-Path (Join-Path (Split-Path -Parent $workspaceRoot) "FOCUS_MASTER_AI")) {
    Copy-Item -Recurse -Force (Join-Path (Split-Path -Parent $workspaceRoot) "FOCUS_MASTER_AI") (Join-Path $stagingDir "FOCUS_MASTER_AI")
}

$gitDir = Join-Path $stagingDir "Focus--Master\\.git"
if (Test-Path $gitDir) {
    Remove-Item -Recurse -Force $gitDir
}

$pathsToStrip = @(
    (Join-Path $stagingDir "Focus--Master\\.secrets"),
    (Join-Path $stagingDir "Focus--Master\\secrets"),
    (Join-Path $stagingDir "Focus--Master\\.pytest_cache"),
    (Join-Path $stagingDir "Focus--Master\\__pycache__")
)

foreach ($path in $pathsToStrip) {
    if (Test-Path $path) {
        Remove-Item -Recurse -Force $path
    }
}

Get-ChildItem -Path (Join-Path $stagingDir "Focus--Master") -Recurse -Force -Filter "__pycache__" | ForEach-Object {
    Remove-Item -Recurse -Force $_.FullName
}

Get-ChildItem -Path (Join-Path $stagingDir "Focus--Master") -Force | Where-Object {
    $_.Name -like ".env*"
} | ForEach-Object {
    Remove-Item -Recurse -Force $_.FullName
}

Compress-Archive -Path (Join-Path $stagingDir "*") -DestinationPath $archivePath -Force
Remove-Item -Recurse -Force $stagingDir

Write-Output $archivePath
