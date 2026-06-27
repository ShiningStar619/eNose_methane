# Export eNose User Guide to PDF (requires pandoc)
# Usage (from repo root):
#   .\docs\user-guide\scripts\export_pdf.ps1

$ErrorActionPreference = "Stop"
$Guide = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Out = Join-Path $Guide "eNose-User-Guide.pdf"

$Files = @(
    (Join-Path $Guide "README.md"),
    (Join-Path $Guide "01-before-you-start.md"),
    (Join-Path $Guide "02-quick-start.md"),
    (Join-Path $Guide "03-gui-overview.md"),
    (Join-Path $Guide "04-settings.md"),
    (Join-Path $Guide "05-manual-mode.md"),
    (Join-Path $Guide "06-results-and-data.md"),
    (Join-Path $Guide "07-troubleshooting.md")
)

$pandoc = Get-Command pandoc -ErrorAction SilentlyContinue
if (-not $pandoc) {
    Write-Error "pandoc not found. Install: winget install JohnMacFarlane.Pandoc"
}

Push-Location $Guide
try {
    & pandoc @Files `
        -o $Out `
        --resource-path=. `
        -V lang=th `
        --toc `
        --toc-depth=2 `
        -V geometry:margin=2.5cm
    Write-Host "Wrote $Out"
} finally {
    Pop-Location
}
