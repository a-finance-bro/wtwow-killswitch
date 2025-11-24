# Example: Screenshot on Trigger

This cross-platform example takes a screenshot when the USB is removed.

## Installation

Copy this function into your `sequences.py` file and add it to the `SEQUENCES` dictionary.

## Code

```python
import platform
import subprocess
from datetime import datetime

def take_screenshot():
    """Takes a screenshot when triggered."""
    system = platform.system()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if system == "Darwin":  # macOS
        filename = f"/tmp/killswitch_screenshot_{timestamp}.png"
        subprocess.run(["screencapture", "-x", filename], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif system == "Windows":
        # Windows screenshot using PowerShell
        filename = f"%TEMP%\\killswitch_screenshot_{timestamp}.png"
        ps_script = f'''
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.SendKeys]::SendWait("%{{PRTSC}}")
        '''
        subprocess.run(["powershell", "-Command", ps_script], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif system == "Linux":
        # Linux screenshot using scrot (must be installed)
        filename = f"/tmp/killswitch_screenshot_{timestamp}.png"
        subprocess.run(["scrot", filename], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Add to SEQUENCES dictionary in sequences.py:
# "Take Screenshot": take_screenshot
```

## Notes

- On Linux, requires `scrot` to be installed (`sudo apt-get install scrot`)
- Screenshots are saved to temp directory
- Useful for evidence/logging purposes
