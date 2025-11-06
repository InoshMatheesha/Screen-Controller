# ================================================================
# DEBUG VERSION - Shows errors, doesn't close
# ================================================================
# Run this on 2nd laptop to see what's wrong
# ================================================================

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  RCPY CLIENT - DEBUG MODE" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Configuration
$serverIP = "192.168.8.158"
$serverPort = 5555
$githubURL = "https://raw.githubusercontent.com/InoshMatheesha/Screen-Controller/refs/heads/main/client.ps1"

Write-Host "[1] Downloading client.ps1 from GitHub..." -ForegroundColor Yellow
try {
    $scriptContent = (New-Object Net.WebClient).DownloadString($githubURL)
    Write-Host "    ✓ Downloaded successfully!" -ForegroundColor Green
    Write-Host "    Script size: $($scriptContent.Length) bytes" -ForegroundColor Gray
} catch {
    Write-Host "    ✗ DOWNLOAD FAILED!" -ForegroundColor Red
    Write-Host "    Error: $_" -ForegroundColor Red
    Write-Host "`nPress any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Host "`n[2] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "    ✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "    ✗ Python NOT installed!" -ForegroundColor Red
    Write-Host "    Install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "`nPress any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Host "`n[3] Checking required packages..." -ForegroundColor Yellow
$packages = @("pyautogui", "cv2", "numpy", "PIL")
$missingPackages = @()

foreach ($pkg in $packages) {
    $check = python -c "import $pkg" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "    ✗ Missing: $pkg" -ForegroundColor Red
        $missingPackages += $pkg
    } else {
        Write-Host "    ✓ Found: $pkg" -ForegroundColor Green
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "`n[!] Installing missing packages..." -ForegroundColor Yellow
    Write-Host "    This may take a few minutes..." -ForegroundColor Gray
    
    $installMap = @{
        "cv2" = "opencv-python"
        "PIL" = "pillow"
    }
    
    foreach ($pkg in $missingPackages) {
        $installName = if ($installMap[$pkg]) { $installMap[$pkg] } else { $pkg }
        Write-Host "    Installing $installName..." -ForegroundColor Cyan
        pip install $installName --quiet
    }
    Write-Host "    ✓ Packages installed!" -ForegroundColor Green
}

Write-Host "`n[4] Testing connection to server..." -ForegroundColor Yellow
Write-Host "    Server: $serverIP`:$serverPort" -ForegroundColor Gray
try {
    $tcpClient = New-Object System.Net.Sockets.TcpClient
    $tcpClient.Connect($serverIP, $serverPort)
    $tcpClient.Close()
    Write-Host "    ✓ Server is reachable!" -ForegroundColor Green
} catch {
    Write-Host "    ✗ Cannot reach server!" -ForegroundColor Red
    Write-Host "    Make sure server is running on $serverIP" -ForegroundColor Yellow
    Write-Host "    Error: $_" -ForegroundColor Red
    Write-Host "`nPress any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Host "`n[5] Starting client..." -ForegroundColor Yellow
Write-Host "    Connecting to: $serverIP`:$serverPort" -ForegroundColor Gray
Write-Host "    Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

# Set variables for script
$c = $serverIP
$p = $serverPort

# Execute the script
try {
    Invoke-Expression $scriptContent
} catch {
    Write-Host "`n✗ CLIENT ERROR!" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host "`nPress any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

Write-Host "`nClient stopped." -ForegroundColor Gray
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
