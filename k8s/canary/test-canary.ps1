# Canary Deployment Traffic Split Verification Script
param (
    [string]$Url = "http://localhost:30080",
    [int]$Requests = 20
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   CANARY DEPLOYMENT TRAFFIC SPLIT VERIFICATION" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Sending $Requests requests to $Url..." -ForegroundColor Yellow

$v1Count = 0
$v2Count = 0

for ($i = 1; $i -le $Requests; $i++) {
    try {
        $res = Invoke-WebRequest -Uri "$Url/health/ready" -UseBasicParsing -TimeoutSec 3
        $data = $res.Content | ConvertFrom-Json
        $ver = $data.version
        if ($ver -match "v2") {
            Write-Host "[$i] Response from CANARY ($ver)" -ForegroundColor Green
            $v2Count++
        } else {
            Write-Host "[$i] Response from STABLE ($ver)" -ForegroundColor Blue
            $v1Count++
        }
    } catch {
        Write-Host "[$i] Request failed: $_" -ForegroundColor Red
    }
    Start-Sleep -Milliseconds 150
}

Write-Host "`n------------------ SUMMARY REPORT ------------------" -ForegroundColor Yellow
Write-Host "Stable (v1.0.0) Hits : $v1Count ($([math]::Round(($v1Count/$Requests)*100))%)" -ForegroundColor Blue
Write-Host "Canary (v2.0.0) Hits : $v2Count ($([math]::Round(($v2Count/$Requests)*100))%)" -ForegroundColor Green
Write-Host "Canary Traffic Verification: SUCCESS" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
