import os
import sys
import time

def get_anchor_path():
    """
    Returns the directory where the script is running.
    This is assumed to be on the USB drive.
    """
    # If frozen (PyInstaller), use executable path
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(sys.executable)
        # On macOS, if we are in a .app bundle, we want the directory containing the .app
        if "Contents/MacOS" in path:
            # Go up 3 levels: Contents/MacOS -> Contents -> .app -> Parent Dir
            path = os.path.abspath(os.path.join(path, "../../.."))
        return path
    # Otherwise use script path
    return os.path.dirname(os.path.abspath(__file__))

def is_drive_present(path):
    """
    Checks if the anchor path still exists.
    Returns True if present, False if removed.
    """
    try:
        return os.path.exists(path)
    except OSError:
        # If an OS error occurs (e.g. device unavailable), assume removed
        return False
