$ErrorActionPreference = 'Stop'
$source = Split-Path -Parent $MyInvocation.MyCommand.Path
$target = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills/minimax-h3-comfyui' } else { Join-Path $HOME '.codex/skills/minimax-h3-comfyui' }
New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null
New-Item -ItemType Directory -Force -Path $target | Out-Null
Get-ChildItem -LiteralPath $source -Force | Where-Object { $_.Name -notin @('.git','__pycache__') } | Copy-Item -Destination $target -Recurse -Force
Write-Output "Installed to $target"
