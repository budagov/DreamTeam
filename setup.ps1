# DreamTeam — one-command setup after clone
# Run from DreamTeam folder: .\setup.ps1

$ErrorActionPreference = "Stop"
Write-Host "DreamTeam setup..." -ForegroundColor Cyan

pip install -e .
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host ""
Write-Host "Verifying..." -ForegroundColor Cyan
python -m dreamteam 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { exit 1 }

if (-not (Test-Path ".dreamteam")) {
    Write-Host ""
    Write-Host "Creating project..." -ForegroundColor Cyan
    python -m dreamteam new-project .
    if ($LASTEXITCODE -ne 0) { exit 1 }
}

Write-Host ""
Write-Host "Ready. For a CLEAN project: cd your-folder; dreamteam new-project ." -ForegroundColor Green
Write-Host "  Or open this folder in Cursor for quick try: /start + goal, dreamteam run-next" -ForegroundColor Gray
