# Sync project source to Raspberry Pi via rsync.
#
# Usage:
#   .\scripts\sync_to_pi.ps1 -Remote "pi@raspberrypi.local" -Dest "~/eNose_methane"

param(
    [Parameter(Mandatory = $true)]
    [string]$Remote,

    [Parameter(Mandatory = $true)]
    [string]$Dest
)

$Root = Split-Path $PSScriptRoot -Parent

$Rsync = Get-Command rsync -ErrorAction SilentlyContinue
if (-not $Rsync) {
    Write-Warning "rsync not found. Install rsync (e.g. via Git for Windows) or use scripts/sync_to_pi.sh from Linux/WSL."
    exit 1
}

$Excludes = @(
    "--exclude", ".venv/",
    "--exclude", "venv/",
    "--exclude", "__pycache__/",
    "--exclude", ".pytest_cache/",
    "--exclude", ".cursor/",
    "--exclude", "reading/data/*.npz",
    "--exclude", "reading/data/*.csv",
    "--exclude", "acquisition/processed_data/",
    "--exclude", "program/cloud_config.json",
    "--exclude", "cloud/upload_queue.json",
    "--exclude", "credentials.json",
    "--exclude", "token.json",
    "--exclude", ".git/"
)

& rsync -av --delete @Excludes "${Root}/" "${Remote}:${Dest}/"
Write-Host "Synced to ${Remote}:${Dest}"
