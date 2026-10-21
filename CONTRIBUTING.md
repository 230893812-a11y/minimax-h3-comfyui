# Contributing

Keep model weights, credentials, private logs, and machine-specific secrets out of commits. Mark hardware claims as verified only when the exact environment and workflow were tested. Run `Get-ChildItem scripts/*.py | ForEach-Object { python -m py_compile $_.FullName }` and `./verify-install.ps1` before opening a pull request.
