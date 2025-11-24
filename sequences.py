import os
import sys
import platform
import subprocess
import ctypes

def lock_device():
    """Locks the workstation."""
    system = platform.system()
    if system == "Windows":
        ctypes.windll.user32.LockWorkStation()
    elif system == "Darwin":  # macOS
        # Try multiple methods for macOS locking
        try:
            subprocess.run(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"], check=False)
        except FileNotFoundError:
            subprocess.run(["pmset", "displaysleepnow"], check=False)
    elif system == "Linux":
        # Try common linux lock commands
        try:
            subprocess.run(["xdg-screensaver", "lock"], check=False)
        except FileNotFoundError:
            try:
                subprocess.run(["gnome-screensaver-command", "-l"], check=False)
            except FileNotFoundError:
                pass # Add more linux lock commands as needed

def shutdown_device():
    """Shuts down the device immediately."""
    system = platform.system()
    if system == "Windows":
        os.system("shutdown /s /t 0")
    elif system == "Darwin" or system == "Linux":
        os.system("shutdown -h now")

def close_all_apps():
    """Closes all user applications (excluding system processes)."""
    system = platform.system()
    
    if system == "Windows":
        # Close all user windows
        # This uses taskkill to close GUI applications
        subprocess.run(["taskkill", "/F", "/FI", "STATUS eq RUNNING", "/FI", "USERNAME eq %USERNAME%"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif system == "Darwin":  # macOS
        # Close all user apps except Finder and System apps
        script = '''
        tell application "System Events"
            set appList to name of every application process whose background only is false
            repeat with appName in appList
                if appName is not in {"Finder", "System Preferences", "System Settings"} then
                    try
                        tell application appName to quit
                    end try
                end if
            end repeat
        end tell
        '''
        subprocess.run(["osascript", "-e", script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif system == "Linux":
        # Close all user GUI applications
        subprocess.run(["pkill", "-u", os.getenv("USER")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Registry of available sequences
SEQUENCES = {
    "Lock Device": lock_device,
    "Shutdown Device": shutdown_device,
    "Close All Apps": close_all_apps
}

def get_sequences():
    """Returns a dictionary of sequence names to functions."""
    return SEQUENCES
