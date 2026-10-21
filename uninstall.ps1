$ErrorActionPreference = 'Stop'
$target = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills/minimax-h3-comfyui' } else { Join-Path $HOME '.codex/skills/minimax-h3-comfyui' }
if (Test-Path -LiteralPath $target) { Remove-Item -LiteralPath $target -Recurse -Force; Write-Output "Removed $target" } else { Write-Output "Not installed: $target" }
