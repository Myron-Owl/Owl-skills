@echo off
setlocal
set "EXCEL_SKILL_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if not exist "%EXCEL_SKILL_PYTHON%" (
  >&2 echo Excel skill Python was not found at "%EXCEL_SKILL_PYTHON%".
  >&2 echo Refresh the configured path using Codex workspace dependencies. Do not fall back to PATH.
  exit /b 2
)
"%EXCEL_SKILL_PYTHON%" %*
exit /b %errorlevel%
