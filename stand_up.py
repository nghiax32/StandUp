import tkinter as tk
from datetime import datetime, timedelta
import threading
from pystray import Icon, Menu, MenuItem
from PIL import Image
import sys

BREAK_TIME_INTERVAL = 60 # minutes
BREAK_TIME_DURATION = 5 # minutes
EYE_TIME_INTERVAL = 20 # minutes
EYE_TIME_DURATION = 2 # minutes

class StandUp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stand Up Reminder")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg="white")

        self.start_time = datetime.now()

        self.timer_label = tk.Label(root, text="", font=("Segoe UI", 20), bg="white")
        self.timer_label.pack()

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Quit", command=self.root.quit)

        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.on_move)
        self.root.bind("<Button-3>", self.show_context_menu)

        self.update_timer()
        
    def start_move(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_move(self, event):
        x = self.root.winfo_x() + (event.x - self.start_x)
        y = self.root.winfo_y() + (event.y - self.start_y)
        self.root.geometry(f"+{x}+{y}")

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def update_timer(self):
        now = datetime.now()
        working_time = now - self.start_time
        working_str = str(working_time).split(".")[0]
        working_str = ":".join(f"{int(x):02}" for x in working_str.split(":"))
        self.timer_label.config(text=working_str)

        self.root.after(1000, self.update_timer)
    
    def on_quit(self, icon, item):
        icon.stop()
        self.root.quit()
        sys.exit()

    def setup_tray(self):
        menu = Menu(MenuItem('Quit', self.on_quit))
        image = Image.open("./icons/systray_icon.jpg").resize((32, 32)) # Replace with your icon path
        icon = Icon("StandUp", image, "StandUp", menu)
        icon.run()

root = tk.Tk()
app = StandUp(root)
threading.Thread(target=app.setup_tray, daemon=True).start()
root.mainloop()