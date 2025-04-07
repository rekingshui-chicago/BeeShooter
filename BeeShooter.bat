@echo off
REM ========================================================
REM Bee Shooter Game - Unified Launcher
REM ========================================================

title Bee Shooter Game

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.6 or higher.
    echo Visit https://www.python.org/downloads/ to download Python.
    pause
    exit /b 1
)

REM Create assets directories if they don't exist
if not exist "assets\sounds" mkdir assets\sounds
if not exist "assets\images" mkdir assets\images

REM Create sound effects
echo Creating sound effects...
python src/utils/create_simple_sounds.py

echo.
echo ========================================================
echo                  BEE SHOOTER GAME
echo ========================================================
echo.
echo Controls:
echo - Arrow keys: Move the fighter
echo - Space: Shoot bullets
echo - M: Launch missiles
echo - B: Use bomb (clears all enemies)
echo - ESC: Quit game
echo - Enter: Restart after game over
echo.
echo Starting game...
echo.

REM Run the game
python main.py %*

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Game exited with an error (code %ERRORLEVEL%).
    echo Check game_debug.log for details.
    pause
)

echo.
echo Thanks for playing!
timeout /t 2 >nul
