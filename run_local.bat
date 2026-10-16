@echo off
title Recetario de Itu v4
cd /d "%~dp0"
python -m http.server 8000 --bind 127.0.0.1
pause
