# WTWOW Universal KillSwitch

A lightweight, cross-platform "Dead Man's Switch" for your computer. Run this app from a USB flash drive, arm it, and if the drive is removed, the computer will instantly lock, shut down, or close all applications.

## Features
- **Cross-Platform**: Works on Windows, macOS, and Linux.
- **Background Operation**: Runs silently in menu bar (macOS) or system tray (Windows/Linux).
- **Visual Indicators**: Green icon = Disarmed, Red icon = Armed.
- **Plug & Play**: Designed to run directly from a USB drive.
- **Open Source**: AGPL 3.0 Licensed.

## Installation & Usage

1.  **Download**: Clone this repository or download the source code to your USB flash drive.
2.  **Dependencies**: Install required packages.
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run**:
    
    **Option A - Using the launcher (Easiest):**
    ```bash
    ./launch.sh
    ```
    The launcher will automatically check dependencies and start the app.
    
    **Option B - Run directly:**
    ```bash
    python3 main.py
    ```
    
    - **macOS**: A 🟢 icon will appear in the menu bar (top-right)
    - **Windows/Linux**: An icon will appear in the system tray
4.  **Arming**:
    - Click the icon in the menu bar/system tray.
    - Select a sequence from the "Select Sequence" or "Sequence" menu.
    - Click "ARM". The icon will change from 🟢 (green) to 🔴 (red).
5.  **Trigger**:
    - Once armed, the app runs in the background.
    - Pull the USB drive out, and the selected action executes immediately.
6.  **Quitting**:
    - You cannot quit while ARMED (safety feature).
    - Disarm first, then select "Quit" from the menu.

## Building a Standalone App (PyInstaller)
To make the app easier to run on different computers without installing Python, you can package it into a standalone executable.

1.  **Install PyInstaller**:
    ```bash
    pip install pyinstaller
    ```
2.  **Build**:
    
    **Option A - Using the spec file (Recommended):**
    ```bash
    pyinstaller killswitch.spec
    ```
    
    **Option B - Command line:**
    ```bash
    # macOS
    pyinstaller --onefile --windowed --name "WTWOW-KillSwitch" main.py
    
    # Windows/Linux
    pyinstaller --onefile --noconsole --name "WTWOW-KillSwitch" main.py
    ```
    
3.  **Deploy**:
    - **macOS**: Go to `dist/` and copy the `.app` file to your USB drive
    - **Windows/Linux**: Go to `dist/` and copy the executable to your USB drive
    - You can now run it on any compatible computer without installing Python or dependencies!

**Note**: On macOS, you may need to allow the app in System Preferences → Security & Privacy on first run.

## Built-in Sequences
For simplicity and safety, only 3 core sequences are included by default:
1.  **Lock Device**: Locks the screen (Requires password to re-enter).
2.  **Shutdown Device**: Immediately powers off the computer.
3.  **Close All Apps**: Force quits all user applications (excluding system processes).

*Note: Risky sequences like "Wipe Drive" are not included by default to prevent accidents.*

## Adding Custom Sequences
You can add your own sequences by editing `sequences.py` or submitting a PR to the `use-cases` folder.

### Sequence Format
To add a new sequence, define a function in `sequences.py` and add it to the `SEQUENCES` dictionary.

```python
def my_custom_sequence():
    # Do something
    print("Triggered!")

SEQUENCES = {
    # ... existing ...
    "My Custom Action": my_custom_sequence
}
```

## Community Use Cases
The `use-cases/` directory contains community-contributed sequences for various platforms and purposes.

### Directory Structure
- `use-cases/macos/` - macOS-specific sequences
- `use-cases/windows/` - Windows-specific sequences
- `use-cases/linux/` - Linux-specific sequences
- `use-cases/cross-platform/` - Cross-platform sequences

### Example Ideas
- 🔊 Play an alert sound
- 📧 Send an email notification
- 📸 Take a screenshot
- 🗑️ Clear clipboard
- 🔐 Encrypt specific files
- 💾 Create a backup snapshot

### Contributing
Want to share your sequence? See [`use-cases/CONTRIBUTING.md`](use-cases/CONTRIBUTING.md) for guidelines on submitting your own sequences!

**Note**: I (the project maintainer) will occasionally add macOS-specific use cases as I develop them for my own workflow.

## Troubleshooting

### App closes immediately on macOS
If the app launches and immediately closes:
1. **Check the log file**: Look for `killswitch_debug.log` in the same directory as the app
2. **Run from Terminal**: This will show any error messages:
   ```bash
   cd /Volumes/YourUSBDrive/
   python3 main.py
   ```
3. **Common fixes**:
   - Make sure all dependencies are installed: `pip3 install -r requirements.txt`
   - On macOS, you may need to grant Accessibility permissions in System Preferences

### Can't see the menu bar icon
- The icon appears as 🟢 (green circle) in the top-right menu bar on macOS
- It may be hidden if your menu bar is crowded - try closing other menu bar apps
- Hold **⌘ (Command)** and drag other icons to rearrange them

### App won't quit
- This is intentional! You must **disarm** the killswitch first
- Click the menu bar icon → select "DISARM" → then "Quit"

### USB removal not detected
- Make sure you're running the app FROM the USB drive (not from your computer)
- The app monitors the directory it's running from
- Test by arming the app and safely ejecting the drive

### PyInstaller build fails
- Make sure PyInstaller is installed: `pip3 install pyinstaller`
- On macOS, you may need to run: `xcode-select --install`
- Try cleaning the build: `rm -rf build dist` then rebuild

## License
This project is licensed under the **AGPL 3.0** License. See [LICENSE](LICENSE) for details.
