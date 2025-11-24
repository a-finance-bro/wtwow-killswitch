#!/bin/bash
# WTWOW Universal KillSwitch Launcher Script
# This script makes it easy to run the killswitch from your USB drive

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Please install Python 3 from https://www.python.org/"
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import rumps" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt --user
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Launch the app
echo "Starting WTWOW Universal KillSwitch..."
echo "Look for the 🟢 icon in your menu bar!"
python3 main.py

# If we get here, the app exited (shouldn't happen normally)
echo "KillSwitch stopped."
read -p "Press Enter to exit..."
