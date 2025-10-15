# API Testing Script for Alert Triage Backend
# Run this in a NEW PowerShell window while server is running

Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Testing Alert Triage Backend API" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "[TEST 1] Health Check..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get
    Write-Host "✅ PASSED: Server is healthy" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json)" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 2: Ingest Alert
Write-Host "[TEST 2] Ingest Alert..." -ForegroundColor Yellow
$alertData = Get-Content ".\data\alerts.json" -Raw
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/alerts/ingest" -Method Post -Body $alertData -ContentType "application/json"
    Write-Host "✅ PASSED: Alert ingested successfully" -ForegroundColor Green
    Write-Host "Alert ID: $($response.alert_id)" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 3: List Alerts
Write-Host "[TEST 3] List Alerts..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/alerts" -Method Get
    Write-Host "✅ PASSED: Retrieved $($response.count) alerts" -ForegroundColor Green
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 4: Analyze Alert with Gemini
Write-Host "[TEST 4] Analyze Alert (This will call Gemini API)..." -ForegroundColor Yellow
Write-Host "⏳ This may take 10-15 seconds..." -ForegroundColor Gray
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/alerts/INC0012345/analyze" -Method Post
    Write-Host "✅ PASSED: Analysis completed" -ForegroundColor Green
    Write-Host "Root Cause: $($response.plan.root_cause)" -ForegroundColor Cyan
    Write-Host "Confidence: $([math]::Round($response.plan.confidence * 100, 0))%" -ForegroundColor Cyan
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Note: Check if GEMINI_API_KEY is set correctly in .env" -ForegroundColor Yellow
}
Write-Host ""

# Test 5: Get Remediation Plan
Write-Host "[TEST 5] Get Remediation Plan..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/alerts/INC0012345/plan" -Method Get
    Write-Host "✅ PASSED: Retrieved remediation plan" -ForegroundColor Green
    Write-Host "Steps: $($response.steps.Count) remediation steps" -ForegroundColor Gray
    Write-Host "Safety Checks: $($response.safety_checks.Count) checks" -ForegroundColor Gray
    Write-Host "Estimated Time: $($response.estimated_time)" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 6: Execute Remediation (Demo Mode)
Write-Host "[TEST 6] Execute Remediation Script (Demo Mode)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/alerts/INC0012345/execute?approved=true" -Method Post
    Write-Host "✅ PASSED: Script executed successfully" -ForegroundColor Green
    Write-Host "Status: $($response.status)" -ForegroundColor Cyan
    Write-Host "MTTR: $($response.mttr_minutes) minutes" -ForegroundColor Cyan
    Write-Host "Output Preview:" -ForegroundColor Gray
    Write-Host "$($response.output.Substring(0, [Math]::Min(200, $response.output.Length)))..." -ForegroundColor DarkGray
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 7: Get Statistics
Write-Host "[TEST 7] Get System Statistics..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/stats" -Method Get
    Write-Host "✅ PASSED: Retrieved statistics" -ForegroundColor Green
    Write-Host "Total Alerts: $($response.total_alerts)" -ForegroundColor Gray
    Write-Host "Analyzed: $($response.analyzed)" -ForegroundColor Gray
    Write-Host "Executed: $($response.executed)" -ForegroundColor Gray
    Write-Host "Success Rate: $([math]::Round($response.success_rate, 1))%" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✨ Testing Complete!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Next Steps:" -ForegroundColor Yellow
Write-Host "1. If Test 4 passed: Gemini API is working! ✅" -ForegroundColor White
Write-Host "2. Open http://localhost:8000/docs to see interactive API docs" -ForegroundColor White
Write-Host "3. Ready to build frontend UI (Phase 2)" -ForegroundColor White
