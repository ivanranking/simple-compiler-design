@echo off
REM SimpleScript Compiler - Professional Edition Launcher

echo.
echo ============================================
echo  🔧 SimpleScript Compiler Professional
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [✓] Python found
python --version
echo.

REM Start the server in background
echo [*] Starting compiler server...
cd backend
start /B python simple_server.py

REM Wait for server to start
timeout /t 2 /nobreak > nul

REM Open browser
echo [✓] Server started successfully!
echo.
echo Opening interface selector in your browser...
start http://localhost:5000

echo.
echo ============================================
echo  ✅ Server is running!
echo ============================================
echo.
echo 📖 Interface Selector: http://localhost:5000
echo 💼 Professional Edition: http://localhost:5000/pro.html
echo 📚 Educational Edition: http://localhost:5000/index.html
echo.
echo Press Ctrl+C in the server terminal to stop
echo.

REM Keep window open
pause