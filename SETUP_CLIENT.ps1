# ================================================================
# QUICK FIX SCRIPT - Installs all requirements automatically
# ================================================================
# Run this on 2nd laptop BEFORE trying to connect
# ================================================================

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  RCPY - Auto Setup Script" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check Python
Write-Host "[1/3] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "      ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "      ✗ Python not found!" -ForegroundColor Red
    Write-Host "`nPlease install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation!" -ForegroundColor Yellow
    pause
    exit
}

# Install packages
Write-Host "`n[2/3] Installing required packages..." -ForegroundColor Yellow
Write-Host "      This may take 2-5 minutes..." -ForegroundColor Gray

$packages = @("pyautogui", "opencv-python", "numpy", "pillow")
foreach ($pkg in $packages) {
    Write-Host "      Installing $pkg..." -ForegroundColor Cyan
    pip install $pkg --quiet --disable-pip-version-check
    if ($LASTEXITCODE -eq 0) {
        Write-Host "      ✓ $pkg installed" -ForegroundColor Green
    } else {
        Write-Host "      ✗ Failed to install $pkg" -ForegroundColor Red
    }
}

# Verify installation
Write-Host "`n[3/3] Verifying installation..." -ForegroundColor Yellow
$allGood = $true
$checkList = @{
    "pyautogui" = "pyautogui"
    "opencv-python" = "cv2"
    "numpy" = "numpy"
    "pillow" = "PIL"
}

foreach ($entry in $checkList.GetEnumerator()) {
    $result = python -c "import $($entry.Value)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "      ✓ $($entry.Key)" -ForegroundColor Green
    } else {
        Write-Host "      ✗ $($entry.Key) - FAILED" -ForegroundColor Red
        $allGood = $false
    }
}

Write-Host ""
if ($allGood) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  ✓ Setup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now run:" -ForegroundColor Cyan
    Write-Host "  - DEBUG_TEST.bat (to test connection)" -ForegroundColor White
    Write-Host "  - Or use the PowerShell command" -ForegroundColor White
} else {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  ✗ Setup Failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Try manual installation:" -ForegroundColor Yellow
    Write-Host "  pip install pyautogui opencv-python numpy pillow" -ForegroundColor White
}

Write-Host ""
pause
