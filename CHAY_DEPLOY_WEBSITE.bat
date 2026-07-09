@echo off
cd /d "%~dp0"
set VIETNT_DEPLOY_SKIP_PY_PAUSE=1
python deploy_site.py
pause
