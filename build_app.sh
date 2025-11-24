#!/bin/bash
# WTWOW Universal KillSwitch - Build Script
# This script builds a standalone .app bundle using PyInstaller

echo "=========================================="
echo "WTWOW Universal KillSwitch - Build Script"
echo "=========================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "PyInstaller is not installed. Installing now..."
    pip3 install pyinstaller --user
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install PyInstaller"
        exit 1
    fi
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Build the app
echo "Building WTWOW-KillSwitch.app..."
python3 -m PyInstaller killswitch.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ BUILD SUCCESSFUL!"
    echo "=========================================="
    echo ""
    echo "Your app is ready at:"
    echo "  $SCRIPT_DIR/dist/WTWOW-KillSwitch.app"
    echo ""
    echo "To use it:"
    echo "  1. Copy the .app to your USB drive"
    echo "  2. Double-click to run"
    echo "  3. Look for the 🟢 icon in your menu bar"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ BUILD FAILED"
    echo "=========================================="
    echo ""
    echo "Check the error messages above."
    exit 1
fi
