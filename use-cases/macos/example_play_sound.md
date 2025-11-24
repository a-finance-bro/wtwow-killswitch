# Example: Play Alert Sound on macOS

This is an example sequence that plays a system alert sound when the USB drive is removed.

## Installation

Copy this function into your `sequences.py` file and add it to the `SEQUENCES` dictionary.

## Code

```python
import subprocess

def play_alert_sound():
    """Plays a system alert sound (macOS only)."""
    # Play the system "Basso" sound
    subprocess.run(["afplay", "/System/Library/Sounds/Basso.aiff"], 
                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Add to SEQUENCES dictionary in sequences.py:
# "Play Alert Sound": play_alert_sound
```

## Usage

1. Add the function to `sequences.py`
2. Update the `SEQUENCES` dictionary
3. Restart the app
4. Select "Play Alert Sound" from the menu
5. Arm and test!
