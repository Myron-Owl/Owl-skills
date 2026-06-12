# Install all skills in this collection to ~/.claude/skills/
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$SkillsDir = "$env:USERPROFILE\.claude\skills"

Write-Host "Installing Owl's Skills to $SkillsDir..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null

# Copy each skill subdirectory that has a SKILL.md
Get-ChildItem -Path $ScriptDir -Directory | ForEach-Object {
    $name = $_.Name
    if ($name -match '^\.') { return }
    $skillFile = Join-Path $_.FullName "SKILL.md"
    if (Test-Path $skillFile) {
        Write-Host "  → Installing: $name" -ForegroundColor Yellow
        $dest = Join-Path $SkillsDir $name
        New-Item -ItemType Directory -Force -Path $dest | Out-Null
        Copy-Item -Recurse -Force "$($_.FullName)\*" "$dest\"
    }
}

Write-Host ""
Write-Host "✅ Done! Restart Claude Code and type / to see your skills." -ForegroundColor Green
