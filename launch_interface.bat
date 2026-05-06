@echo off
title SimpleScript Compiler

echo ============================================
echo     🚀 Starting SimpleScript Compiler...
echo ============================================
echo.

cd /d "%~dp0backend"
python simple_server.py
pause