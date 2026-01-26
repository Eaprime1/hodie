# Add-SessionNote.ps1
# PowerShell version of session notes script
# Usage: pwsh Add-SessionNote.ps1 "Your note here"

param(
    [Parameter(Mandatory=$true)]
    [string]$Note
)

$SessionDate = Get-Date -Format "yyyy-MM-dd"
$Timestamp = Get-Date -Format "HH:mm:ss"
$NotesFile = "/home/user/Q/hodie/.eric/session_notes_$SessionDate.md"

# Create file if doesn't exist
if (-not (Test-Path $NotesFile)) {
    $header = @"
# Session Notes - $SessionDate

**Environment**: New Laptop (faster machine)
**Q Path**: /home/user/Q/
**Shell**: PowerShell $($PSVersionTable.PSVersion)

---

"@
    Set-Content -Path $NotesFile -Value $header
}

# Append note with timestamp
$noteEntry = @"

## [$Timestamp] $Note

"@

Add-Content -Path $NotesFile -Value $noteEntry

Write-Host "✓ Note appended to $NotesFile" -ForegroundColor Green
Write-Host "`nRecent notes:" -ForegroundColor Cyan
Get-Content $NotesFile | Select-Object -Last 10
