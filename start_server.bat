@echo off
cd /d "%~dp0"
python package_for_pages.py
echo.
echo Сайт: http://127.0.0.1:8765/
python -m http.server 8765 --directory _site
