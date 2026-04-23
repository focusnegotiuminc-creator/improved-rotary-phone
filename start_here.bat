@echo off
setlocal

set "WORKSPACE=G:\My Drive\FOCUS_MASTER_AI_live"

if not exist "%WORKSPACE%" (
  echo Workspace not found:
  echo %WORKSPACE%
  pause
  exit /b 1
)

cd /d "%WORKSPACE%"

title FOCUS Master AI Workspace

echo.
echo FOCUS Master AI workspace is ready.
echo.
echo Workspace:
echo %WORKSPACE%
echo.
echo Recommended resume flow:
echo   1. Open Codex/Desktop and choose this folder as the workspace.
echo   2. Read WORKSPACE_BOOT.md if you need the handoff notes.
echo   3. Run git status
echo   4. Run git pull
echo   5. Continue work on the current branch
echo.
echo Useful commands:
echo   cd /d "%WORKSPACE%"
echo   git status
echo   git pull
echo   python app.py
echo.
echo Opening this folder in Explorer...
start "" explorer.exe "%WORKSPACE%"

echo Opening the workspace boot note...
start "" notepad.exe "%WORKSPACE%\WORKSPACE_BOOT.md"

echo.
echo Current branch status:
git status --short --branch
echo.
pause

