$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$localHugo = Join-Path $root '.tools/hugo.exe'
if (Test-Path $localHugo) { $hugoExe = $localHugo } else { $hugoExe = 'hugo' }
& $hugoExe --source $root --destination public --gc --minify --cleanDestinationDir
if ($LASTEXITCODE -ne 0) { throw 'Hugo build failed' }
Write-Host 'Built production site in public/'
