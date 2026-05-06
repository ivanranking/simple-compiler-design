@echo off
title SimpleScript Compiler

echo Starting SimpleScript Compiler...
cd /d "%~dp0backend"
python simple_server.py
pause