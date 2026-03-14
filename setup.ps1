# DreamTeam — quick setup after clone
# Run from DreamTeam folder: .\setup.ps1

$ErrorActionPreference = "Stop"
Write-Host "DreamTeam setup..." -ForegroundColor Cyan

pip install -e .
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host ""
Write-Host "Verifying..." -ForegroundColor Cyan
python -m dreamteam 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host "OK. Use: python -m dreamteam new-project ." -ForegroundColor Green
Write-Host "  or: dreamteam new-project <path>" -ForegroundColor Green
