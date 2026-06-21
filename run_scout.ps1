# Weekly Zurich Events Scout
# Invoked by Windows Task Scheduler every Sunday at 18:00 Europe/Zurich

$Dir     = "C:\Users\gusta\zurich-events-scout"
$LogFile = "$Dir\scout-log.txt"
$Stamp   = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Add-Content $LogFile "`n[$Stamp] === Starting Zurich Events Scout ==="

# Step 1: Run research - searches web, updates zurich-events-tracker.json
Add-Content $LogFile "[$Stamp] Research phase starting (may take 20-30 min)"
Get-Content "$Dir\research_prompt.md" -Raw | claude --print --allowed-tools "WebSearch,WebFetch,Read,Write"
$ResearchExit = $LASTEXITCODE
Add-Content $LogFile "[$Stamp] Research phase finished (exit $ResearchExit)"

if ($ResearchExit -eq 0) {
    # Step 2: Build email HTML from tracker and send via SMTP
    Add-Content $LogFile "[$Stamp] Sending email"
    python3 "$Dir\generate_and_send.py"
    $SendExit = $LASTEXITCODE
    Add-Content $LogFile "[$Stamp] Send finished (exit $SendExit)"
} else {
    Add-Content $LogFile "[$Stamp] Research failed - skipping email send"
}
