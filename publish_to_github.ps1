# First-time publish to GitHub Pages (branch main).
# Run: powershell -ExecutionPolicy Bypass -File .\publish_to_github.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$gh = Join-Path ${env:ProgramFiles} "GitHub CLI\gh.exe"
if (-not (Test-Path $gh)) {
    Write-Host "Install GitHub CLI: winget install GitHub.cli"
    exit 1
}

& $gh auth status 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "GitHub login required (browser will open)."
    & $gh auth login -h github.com -p https -w
}

$repoName = "vyacheslav-ege-audit"
$ErrorActionPreference = "Continue"
$remoteUrl = git remote get-url origin 2>$null
$ErrorActionPreference = "Stop"
if ($LASTEXITCODE -eq 0 -and $remoteUrl) {
    Write-Host "Remote exists, pushing..."
    git push -u origin main
    Write-Host "Done. Enable Pages: Settings -> Pages -> Source: GitHub Actions."
    exit 0
}

Write-Host "Creating repo $repoName and pushing..."
& $gh repo create $repoName --public --source . --remote origin --push
$user = & $gh api user -q .login 2>$null
Write-Host "Repo: https://github.com/$user/$repoName"
Write-Host "Site: https://$user.github.io/$repoName/"
Write-Host "Settings -> Pages -> Build and deployment -> Source: GitHub Actions."
