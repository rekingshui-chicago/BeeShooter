#!/bin/bash
# ========================================================
# Bee Shooter Game - Unified Launcher for Linux
# ========================================================

# Set terminal title
echo -e "\033]0;Bee Shooter Game\007"

# Find Python
if command -v python3 &>/dev/null; then
    PYTHON="python3"
else
    PYTHON="python"
fi

# Check if Python is installed
if ! command -v $PYTHON &> /dev/null; then
    echo "Python is not installed."
    echo "Please install Python 3.6 or higher."
    echo "On Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "On Fedora: sudo dnf install python3 python3-pip"
    read -p "Press Enter to exit..."
    exit 1
fi

# Create assets directories if they don't exist
if [ ! -d "assets/sounds" ]; then
    mkdir -p assets/sounds
fi

if [ ! -d "assets/images" ]; then
    mkdir -p assets/images
fi

# Create sound effects
echo "Creating sound effects..."
$PYTHON src/utils/create_simple_sounds.py

echo
echo "========================================================"
echo "                  BEE SHOOTER GAME"
echo "========================================================"
echo
echo "Controls:"
echo "- Arrow keys: Move the fighter"
echo "- Space: Shoot bullets"
echo "- M: Launch missiles"
echo "- B: Use bomb (clears all enemies)"
echo "- ESC: Quit game"
echo "- Enter: Restart after game over"
echo
echo "Starting game..."
echo

# Run the game
$PYTHON main.py "$@"

# Check if game exited with an error
if [ $? -ne 0 ]; then
    echo
    echo "Game exited with an error (code $?)."
    echo "Check game_debug.log for details."
    read -p "Press Enter to continue..."
fi

echo
echo "Thanks for playing!"
sleep 2
