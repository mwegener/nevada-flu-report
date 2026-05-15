@echo off
setlocal EnableDelayedExpansion
rem ============== run_pipeline.bat ====================

cd /d "%~dp0"
if not defined VIRTUAL_ENV if exist ".venv\Scripts\activate.bat" call ".venv\Scripts\activate.bat"

if "%~1"=="" goto :usage

set "CMD=%~1"
shift
set "ARGS=%*"

if /I "%CMD%"=="flu" (
    python -m flu_report.main !ARGS!
    goto :eof
) else if /I "%CMD%"=="ilinet" (
    python -m essence_to_ilinet !ARGS!
    goto :eof
)

:usage
echo Usage:
echo   %~n0 flu    [--year 2026 ...]
echo   %~n0 ilinet --start ddMMMyyyy --end ddMMMyyyy ...
exit /b 1