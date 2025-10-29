# Demo PowerShell script for Script Runner Pro
Write-Host "System Information" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green

Write-Host "Computer Name: $env:COMPUTERNAME"
Write-Host "User: $env:USERNAME"
Write-Host "OS: $((Get-WmiObject -Class Win32_OperatingSystem).Caption)"
Write-Host "Architecture: $((Get-WmiObject -Class Win32_OperatingSystem).OSArchitecture)"
Write-Host "PowerShell Version: $($PSVersionTable.PSVersion)"

Write-Host "`nRunning processes:" -ForegroundColor Yellow
Get-Process | Select-Object -First 5 Name, CPU, WorkingSet | Format-Table

Write-Host "Script completed!" -ForegroundColor Green

