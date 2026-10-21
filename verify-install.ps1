$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$required = @('SKILL.md','README.md','LICENSE','scripts/check_models.py','scripts/check_environment.py','scripts/check_output.py','scripts/diagnose.py','examples/models.template.json','references/hardware-matrix.md','workflows/t2v-standard.json')
$missing = @($required | Where-Object { -not (Test-Path (Join-Path $root $_)) })
if ($missing.Count) { Write-Error ('Missing: ' + ($missing -join ', ')); exit 1 }
Write-Output "Skill files verified at $root"
