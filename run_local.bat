@echo off
cd /d "%~dp0"
echo Recetario Video Lab - servidor local en http://localhost:8000
echo Pulsa CTRL+C para parar.
python -m http.server 8000
pause
