$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$branch = git -C $root branch --show-current
if ($branch -ne 'main') { throw 'Publish from the main branch only' }
$staged = git -C $root diff --cached --name-only
if ($staged) { throw 'Commit or unstage existing staged changes before publishing' }
& (Join-Path $PSScriptRoot 'build.ps1')
python (Join-Path $PSScriptRoot 'check_site.py')
if ($LASTEXITCODE -ne 0) { throw 'Site validation failed' }
git -C $root add -- content assets layouts static archetypes hugo.toml
git -C $root diff --cached --quiet
if ($LASTEXITCODE -eq 0) { Write-Host 'No content changes to publish'; exit 0 }
git -C $root commit -m 'docs: publish blog updates'
if ($LASTEXITCODE -ne 0) { throw 'Git commit failed' }
git -C $root push origin main
if ($LASTEXITCODE -ne 0) { throw 'Git push failed' }
Write-Host 'Source pushed. Follow the Publish blog workflow in GitHub Actions.'
