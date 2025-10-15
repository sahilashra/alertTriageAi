# Agentic Alert Triage - Quick Start Script
# Run this to start both backend and frontend

Write-Host "=======================================" -ForegroundColor Green
Write-Host "Starting Agentic Alert Triage Assistant" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "backend\app.py")) {
    Write-Host "ERROR: Please run this from the alert-triage-ai directory" -ForegroundColor Red
    Write-Host "Current directory: $PWD" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "[1/3] Starting Backend Server..." -ForegroundColor Cyan
Write-Host "      - Auto-loading demo alert INC0012345" -ForegroundColor Gray
Write-Host "      - Initializing Gemini AI service" -ForegroundColor Gray
Write-Host ""

# Check for venv
$venvPath = "..\.venv\Scripts\activate.ps1"
if (-not (Test-Path $venvPath)) {
    Write-Host "WARNING: Virtual environment not found" -ForegroundColor Yellow
}

# Start backend in a new window
$backendCommand = @"
cd '$PWD'
if (Test-Path '$venvPath') { & '$venvPath' }
Write-Host 'Backend Server Starting...' -ForegroundColor Green
Write-Host ''
cd backend
python -m uvicorn app:app --reload --port 8000
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCommand

Write-Host "DONE: Backend starting at http://localhost:8000" -ForegroundColor Green
Write-Host ""

# Wait for backend
Write-Host "[2/3] Waiting for backend to initialize..." -ForegroundColor Cyan
Write-Host "      (This takes about 8 seconds)" -ForegroundColor Gray

for ($i = 8; $i -gt 0; $i--) {
    Write-Host "      $i seconds remaining..." -ForegroundColor Gray
    Start-Sleep -Seconds 1
}
Write-Host ""

# Test backend
Write-Host "      Testing backend connection..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get -TimeoutSec 5
    if ($response.status -eq "healthy") {
        Write-Host "DONE: Backend is healthy and ready!" -ForegroundColor Green
        Write-Host "      Gemini configured: $($response.gemini_configured)" -ForegroundColor Gray
    }
} catch {
    Write-Host "WARNING: Backend might still be starting..." -ForegroundColor Yellow
    Write-Host "         Wait 10 more seconds if frontend does not work" -ForegroundColor Gray
}
Write-Host ""

# Open frontend
Write-Host "[3/3] Opening Frontend in browser..." -ForegroundColor Cyan
Start-Process "frontend\index.html"
Write-Host "DONE: Frontend opened" -ForegroundColor Green
Write-Host ""

Write-Host "=======================================" -ForegroundColor Green
Write-Host "Application Started Successfully!" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host ""
Write-Host "URLS:" -ForegroundColor Yellow
Write-Host "  Backend API:  http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs:     http://localhost:8000/docs" -ForegroundColor White
Write-Host "  Frontend:     Opened in your browser" -ForegroundColor White
Write-Host ""
Write-Host "DEMO STEPS:" -ForegroundColor Yellow
Write-Host "  1. Wait for frontend page to load" -ForegroundColor White
Write-Host "  2. You will see CRITICAL disk space alert" -ForegroundColor White
Write-Host "  3. Click 'Start Analysis' button" -ForegroundColor White
Write-Host "  4. AI analyzes for 10-15 seconds" -ForegroundColor White
Write-Host "  5. Review plan and click 'Approve & Execute'" -ForegroundColor White
Write-Host "  6. See results: 4 min MTTR!" -ForegroundColor White
Write-Host ""
Write-Host "TIPS:" -ForegroundColor Yellow
Write-Host "  - Backend window will stay open (do not close it)" -ForegroundColor Gray
Write-Host "  - Press CTRL+C in backend window to stop server" -ForegroundColor Gray
Write-Host "  - Demo alert INC0012345 is pre-loaded" -ForegroundColor Gray
Write-Host ""

Write-Host "Press any key to close this window..." -ForegroundColor DarkGray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
