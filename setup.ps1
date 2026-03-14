# DreamTeam — install engine only (no project here)
# Run from DreamTeam folder: .\setup.ps1

$ErrorActionPreference = "Stop"
Write-Host "DreamTeam setup (engine only)..." -ForegroundColor Cyan

pip install -e .
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host ""
Write-Host "Verifying..." -ForegroundColor Cyan
python -m dreamteam 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { exit 1 }

$scriptsPath = python -c "import sysconfig; print(sysconfig.get_path('scripts'))" 2>$null
if ($scriptsPath -and (Test-Path $scriptsPath)) {
    $env:Path = "$scriptsPath;$env:Path"
    Write-Host ""
    Write-Host "Added Python Scripts to PATH for this session." -ForegroundColor Gray
}

Write-Host ""
Write-Host "Installed. Create project in a SEPARATE folder:" -ForegroundColor Green
Write-Host "  cd C:\Projects\my-app" -ForegroundColor White
Write-Host "  python -m dreamteam new-project ." -ForegroundColor White
Write-Host ""
Write-Host "If 'dreamteam' not found, use: python -m dreamteam <command>" -ForegroundColor Yellow
Write-Host "Do NOT use DreamTeam folder as project - engine and project stay separate." -ForegroundColor Yellow
