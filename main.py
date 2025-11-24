import platform
import sys
import os
import threading
import time
import sequences
import usb_monitor

# Platform detection
PLATFORM = platform.system()

if PLATFORM == "Darwin":
    # macOS - Use rumps for menu bar
    import rumps
    
    class KillSwitchApp(rumps.App):
        def __init__(self):
            super(KillSwitchApp, self).__init__("🔑", quit_button=None)
            self.is_armed = False
            self.monitor_thread = None
            self.stop_event = threading.Event()
            self.anchor_path = usb_monitor.get_anchor_path()
            self.sequences_map = sequences.get_sequences()
            self.selected_sequence = list(self.sequences_map.keys())[0]
            
            # Build menu
            self.build_menu()
            self.update_icon()
        
        def build_menu(self):
            # Sequence selection submenu
            sequence_items = []
            for seq_name in self.sequences_map.keys():
                item = rumps.MenuItem(seq_name, callback=self.select_sequence)
                if seq_name == self.selected_sequence:
                    item.state = True
                sequence_items.append(item)
            
            self.menu = [
                rumps.MenuItem("Status: DISARMED", callback=None),
                rumps.separator,
                ("Select Sequence", sequence_items),
                rumps.separator,
                rumps.MenuItem("ARM", callback=self.toggle_arm),
                rumps.separator,
                rumps.MenuItem(f"Monitoring: {self.anchor_path[:30]}...", callback=None),
                rumps.separator,
                rumps.MenuItem("Quit", callback=self.quit_app)
            ]
        
        def select_sequence(self, sender):
            # Update checkmarks
            for item in self.menu["Select Sequence"].values():
                item.state = False
            sender.state = True
            self.selected_sequence = sender.title
        
        def toggle_arm(self, sender):
            if self.is_armed:
                self.disarm()
            else:
                self.arm()
        
        def arm(self):
            self.is_armed = True
            self.menu["Status: DISARMED"].title = "Status: ARMED"
            self.menu["ARM"].title = "DISARM"
            self.update_icon()
            
            self.stop_event.clear()
            self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.monitor_thread.start()
        
        def disarm(self):
            self.is_armed = False
            self.stop_event.set()
            self.menu["Status: ARMED"].title = "Status: DISARMED"
            self.menu["DISARM"].title = "ARM"
            self.update_icon()
        
        def update_icon(self):
            if self.is_armed:
                self.title = "🔴"  # Red circle for armed
            else:
                self.title = "🟢"  # Green circle for disarmed
        
        def monitor_loop(self):
            while not self.stop_event.is_set():
                if not usb_monitor.is_drive_present(self.anchor_path):
                    self.trigger_sequence()
                    break
                time.sleep(0.5)
        
        def trigger_sequence(self):
            self.disarm()
            action = self.sequences_map.get(self.selected_sequence)
            if action:
                print(f"Triggering sequence: {self.selected_sequence}")
                action()
        
        def quit_app(self, _):
            if self.is_armed:
                rumps.alert("Cannot quit while ARMED", "Please disarm the killswitch first.")
            else:
                rumps.quit_application()

else:
    # Windows/Linux - Use pystray for system tray
    import pystray
    from PIL import Image, ImageDraw
    
    class KillSwitchApp:
        def __init__(self):
            self.is_armed = False
            self.monitor_thread = None
            self.stop_event = threading.Event()
            self.anchor_path = usb_monitor.get_anchor_path()
            self.sequences_map = sequences.get_sequences()
            self.selected_sequence = list(self.sequences_map.keys())[0]
            
            # Create system tray icon
            self.icon = pystray.Icon("killswitch")
            self.icon.icon = self.create_icon(False)
            self.icon.title = "WTWOW KillSwitch - DISARMED"
            self.icon.menu = self.build_menu()
        
        def create_icon(self, armed):
            """Create a simple colored circle icon."""
            width = 64
            height = 64
            color = (255, 0, 0) if armed else (0, 255, 0)  # Red if armed, Green if disarmed
            
            image = Image.new('RGB', (width, height), (0, 0, 0))
            dc = ImageDraw.Draw(image)
            dc.ellipse([8, 8, 56, 56], fill=color)
            
            return image
        
        def build_menu(self):
            # Build sequence selection menu
            sequence_items = []
            for seq_name in self.sequences_map.keys():
                item = pystray.MenuItem(
                    seq_name, 
                    self.make_select_sequence(seq_name),
                    checked=lambda item, n=seq_name: n == self.selected_sequence
                )
                sequence_items.append(item)
            
            return pystray.Menu(
                pystray.MenuItem("Status", None, enabled=False),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Sequence", pystray.Menu(*sequence_items)),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("ARM/DISARM", self.toggle_arm),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Quit", self.quit_app)
            )
        
        def make_select_sequence(self, seq_name):
            def callback(icon, item):
                self.selected_sequence = seq_name
                # Rebuild menu to update checkmarks
                self.icon.menu = self.build_menu()
            return callback
        
        def toggle_arm(self, icon, item):
            if self.is_armed:
                self.disarm()
            else:
                self.arm()
        
        def arm(self):
            self.is_armed = True
            self.icon.icon = self.create_icon(True)
            self.icon.title = "WTWOW KillSwitch - ARMED"
            
            self.stop_event.clear()
            self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.monitor_thread.start()
        
        def disarm(self):
            self.is_armed = False
            self.stop_event.set()
            self.icon.icon = self.create_icon(False)
            self.icon.title = "WTWOW KillSwitch - DISARMED"
        
        def monitor_loop(self):
            while not self.stop_event.is_set():
                if not usb_monitor.is_drive_present(self.anchor_path):
                    self.trigger_sequence()
                    break
                time.sleep(0.5)
        
        def trigger_sequence(self):
            self.disarm()
            action = self.sequences_map.get(self.selected_sequence)
            if action:
                print(f"Triggering sequence: {self.selected_sequence}")
                action()
        
        def quit_app(self, icon, item):
            if self.is_armed:
                print("Cannot quit while ARMED. Please disarm first.")
            else:
                self.icon.stop()
        
        def run(self):
            self.icon.run()


if __name__ == "__main__":
    try:
        # Setup basic logging to catch startup errors
        import logging
        
        # Determine log path - try to put it next to the app, otherwise in tmp
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
            # If in a .app bundle, go up to the bundle root
            if "Contents/MacOS" in base_path:
                base_path = os.path.abspath(os.path.join(base_path, "../../.."))
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        log_file = os.path.join(base_path, "killswitch_debug.log")
        
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        logging.info("Starting KillSwitch App...")
        logging.info(f"Platform: {PLATFORM}")
        logging.info(f"Base Path: {base_path}")

        app = KillSwitchApp()
        if PLATFORM == "Darwin":
            app.run()
        else:
            app.run()
            
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        try:
            logging.error(f"CRITICAL ERROR: {error_msg}")
            print(f"CRITICAL ERROR: {error_msg}")
        except:
            # Last resort if logging fails
            with open(os.path.expanduser("~/killswitch_crash.txt"), "w") as f:
                f.write(error_msg)

