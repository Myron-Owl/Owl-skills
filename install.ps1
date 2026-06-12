# Owl's Skills — 一键安装所有 skill 到 ~/.claude/skills/
#
# 用法:
#   本地安装: git clone ... && .\Owl-skills\install.ps1
#   远程安装: irm https://git.io/... | iex
param()

$Repo = "https://github.com/Myron-Owl/Owl-skills.git"
$SkillsDir = "$env:USERPROFILE\.claude\skills"

# 判断是在本地运行还是远程 (iex)
$IsLocal = $false
if ($MyInvocation.MyCommand.Path) {
    $ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
    $IsLocal = Test-Path (Join-Path $ScriptPath "README.md")
}

if (-not $IsLocal) {
    Write-Host "→ Cloning repository..." -ForegroundColor Cyan
    $TmpDir = Join-Path $env:TEMP "owl-skills-$([System.IO.Path]::GetRandomFileName())"
    git clone --depth 1 $Repo $TmpDir
    if (-not (Test-Path $TmpDir)) {
        Write-Host "❌ Clone failed. Check your network and try again." -ForegroundColor Red
        exit 1
    }
    $ScriptPath = $TmpDir
}

Write-Host "→ Installing Owl's Skills..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null

$count = 0
Get-ChildItem -Path $ScriptPath -Directory | ForEach-Object {
    $name = $_.Name
    if ($name -match '^[\._]') { return }
    $skillFile = Join-Path $_.FullName "SKILL.md"
    if (Test-Path $skillFile) {
        Write-Host "   • $name" -ForegroundColor Yellow
        $dest = Join-Path $SkillsDir $name
        New-Item -ItemType Directory -Force -Path $dest | Out-Null
        Copy-Item -Recurse -Force "$($_.FullName)\*" "$dest\"
        $count++
    }
}

if ($TmpDir -and (Test-Path $TmpDir)) {
    Remove-Item -Recurse -Force $TmpDir -ErrorAction SilentlyContinue
}

Write-Host ""
if ($count -gt 0) {
    Write-Host "✅ Installed $count skill(s)! Restart Claude Code and type / to see them." -ForegroundColor Green
} else {
    Write-Host "⚠️ No skills found to install." -ForegroundColor Yellow
}
