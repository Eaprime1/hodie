# Start-FileServer.ps1
# PowerShell file server for Q/ folder
# Usage: pwsh Start-FileServer.ps1 -Port 8080

param(
    [int]$Port = 8080,
    [string]$Path = ""
)

# Resolve default path at runtime so $HOME is evaluated correctly
if (-not $Path) {
    $Path = Join-Path $HOME "Q"
}

Write-Host @"

📂 Starting PowerShell File Server
===================================
Port:        $Port
Serving:     $Path
Shell:       PowerShell $($PSVersionTable.PSVersion)

Access at:
  http://localhost:$Port/hodie/
  http://localhost:$Port/today/

Stop with: Ctrl+C

"@ -ForegroundColor Cyan

# Check if python3 available
if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
    Write-Error "✗ Python3 not found. Please install it (e.g., 'sudo apt-get install -y python3') and try again."
    exit 1
}

Write-Host "🚀 Starting server...`n" -ForegroundColor Green

Set-Location $Path
python3 -m http.server $Port
