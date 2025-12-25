#!/usr/bin/env python3
"""
Autoclicker Application
A simple, configurable autoclicker with GUI for gaming and automation.
"""

import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Listener as KeyboardListener, Key, KeyCode


class Autoclicker:
    def __init__(self):
        self.mouse = MouseController()
        self.clicking = False
        self.click_thread = None

        # Default settings
        self.click_interval = 0.1  # seconds
        self.click_button = Button.left
        self.click_type = "single"  # single, double
        self.hotkey = Key.f6
        self.use_fixed_position = False
        self.fixed_x = 0
        self.fixed_y = 0

        # Setup GUI
        self.setup_gui()

        # Start keyboard listener
        self.keyboard_listener = KeyboardListener(on_press=self.on_key_press)
        self.keyboard_listener.start()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Autoclicker")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        # Style
        style = ttk.Style()
        style.configure("TLabel", padding=5)
        style.configure("TButton", padding=5)

        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Title
        title_label = ttk.Label(main_frame, text="Autoclicker", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Status indicator
        self.status_var = tk.StringVar(value="Status: Stopped")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var,
                                       font=("Helvetica", 12))
        self.status_label.grid(row=1, column=0, columnspan=2, pady=5)

        # Click interval section
        interval_frame = ttk.LabelFrame(main_frame, text="Click Interval", padding="10")
        interval_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        ttk.Label(interval_frame, text="Interval (ms):").grid(row=0, column=0, sticky="w")
        self.interval_var = tk.StringVar(value="100")
        interval_entry = ttk.Entry(interval_frame, textvariable=self.interval_var, width=10)
        interval_entry.grid(row=0, column=1, padx=5)

        # Quick interval buttons
        quick_frame = ttk.Frame(interval_frame)
        quick_frame.grid(row=1, column=0, columnspan=2, pady=5)

        for ms in [50, 100, 250, 500, 1000]:
            btn = ttk.Button(quick_frame, text=f"{ms}ms", width=6,
                           command=lambda m=ms: self.interval_var.set(str(m)))
            btn.pack(side=tk.LEFT, padx=2)

        # Click button section
        button_frame = ttk.LabelFrame(main_frame, text="Click Button", padding="10")
        button_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        self.button_var = tk.StringVar(value="left")
        ttk.Radiobutton(button_frame, text="Left Click", variable=self.button_var,
                        value="left").grid(row=0, column=0, padx=10)
        ttk.Radiobutton(button_frame, text="Right Click", variable=self.button_var,
                        value="right").grid(row=0, column=1, padx=10)
        ttk.Radiobutton(button_frame, text="Middle Click", variable=self.button_var,
                        value="middle").grid(row=0, column=2, padx=10)

        # Click type section
        type_frame = ttk.LabelFrame(main_frame, text="Click Type", padding="10")
        type_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        self.type_var = tk.StringVar(value="single")
        ttk.Radiobutton(type_frame, text="Single Click", variable=self.type_var,
                        value="single").grid(row=0, column=0, padx=20)
        ttk.Radiobutton(type_frame, text="Double Click", variable=self.type_var,
                        value="double").grid(row=0, column=1, padx=20)

        # Position section
        pos_frame = ttk.LabelFrame(main_frame, text="Click Position", padding="10")
        pos_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

        self.pos_var = tk.StringVar(value="cursor")
        ttk.Radiobutton(pos_frame, text="Current Cursor Position", variable=self.pos_var,
                        value="cursor").grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Radiobutton(pos_frame, text="Fixed Position:", variable=self.pos_var,
                        value="fixed").grid(row=1, column=0, sticky="w")

        coord_frame = ttk.Frame(pos_frame)
        coord_frame.grid(row=1, column=1, sticky="w")

        ttk.Label(coord_frame, text="X:").pack(side=tk.LEFT)
        self.x_var = tk.StringVar(value="0")
        ttk.Entry(coord_frame, textvariable=self.x_var, width=6).pack(side=tk.LEFT, padx=2)

        ttk.Label(coord_frame, text="Y:").pack(side=tk.LEFT, padx=(10, 0))
        self.y_var = tk.StringVar(value="0")
        ttk.Entry(coord_frame, textvariable=self.y_var, width=6).pack(side=tk.LEFT, padx=2)

        # Get current position button
        get_pos_btn = ttk.Button(pos_frame, text="Get Current Position",
                                  command=self.get_current_position)
        get_pos_btn.grid(row=2, column=0, columnspan=2, pady=5)

        # Current position display
        self.cur_pos_var = tk.StringVar(value="")
        ttk.Label(pos_frame, textvariable=self.cur_pos_var).grid(row=3, column=0, columnspan=2)

        # Hotkey section
        hotkey_frame = ttk.LabelFrame(main_frame, text="Hotkey", padding="10")
        hotkey_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

        ttk.Label(hotkey_frame, text="Press F6 to Start/Stop",
                  font=("Helvetica", 10, "bold")).pack()

        # Control buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=15)

        self.start_btn = ttk.Button(btn_frame, text="Start (F6)", width=15,
                                     command=self.toggle_clicking)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        quit_btn = ttk.Button(btn_frame, text="Quit", width=15, command=self.quit_app)
        quit_btn.pack(side=tk.LEFT, padx=5)

        # Update position display periodically
        self.update_position_display()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    def update_position_display(self):
        """Update the current cursor position display."""
        x, y = self.mouse.position
        self.cur_pos_var.set(f"Current cursor: ({x}, {y})")
        self.root.after(100, self.update_position_display)

    def get_current_position(self):
        """Set fixed position to current cursor position."""
        x, y = self.mouse.position
        self.x_var.set(str(x))
        self.y_var.set(str(y))
        self.pos_var.set("fixed")

    def on_key_press(self, key):
        """Handle hotkey press."""
        if key == self.hotkey:
            self.root.after(0, self.toggle_clicking)

    def toggle_clicking(self):
        """Toggle autoclicker on/off."""
        if self.clicking:
            self.stop_clicking()
        else:
            self.start_clicking()

    def start_clicking(self):
        """Start the autoclicker."""
        try:
            interval_ms = int(self.interval_var.get())
            if interval_ms < 10:
                messagebox.showwarning("Warning", "Interval too small! Minimum is 10ms.")
                return
            self.click_interval = interval_ms / 1000.0
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid interval number.")
            return

        # Set click button
        button_map = {
            "left": Button.left,
            "right": Button.right,
            "middle": Button.middle
        }
        self.click_button = button_map.get(self.button_var.get(), Button.left)

        # Set click type
        self.click_type = self.type_var.get()

        # Set position mode
        self.use_fixed_position = self.pos_var.get() == "fixed"
        if self.use_fixed_position:
            try:
                self.fixed_x = int(self.x_var.get())
                self.fixed_y = int(self.y_var.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid X and Y coordinates.")
                return

        self.clicking = True
        self.status_var.set("Status: Running")
        self.start_btn.configure(text="Stop (F6)")

        # Start clicking thread
        self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
        self.click_thread.start()

    def stop_clicking(self):
        """Stop the autoclicker."""
        self.clicking = False
        self.status_var.set("Status: Stopped")
        self.start_btn.configure(text="Start (F6)")

    def click_loop(self):
        """Main clicking loop."""
        while self.clicking:
            # Move to fixed position if enabled
            if self.use_fixed_position:
                self.mouse.position = (self.fixed_x, self.fixed_y)

            # Perform click
            if self.click_type == "double":
                self.mouse.click(self.click_button, 2)
            else:
                self.mouse.click(self.click_button, 1)

            time.sleep(self.click_interval)

    def quit_app(self):
        """Clean up and exit."""
        self.clicking = False
        self.keyboard_listener.stop()
        self.root.destroy()

    def run(self):
        """Start the application."""
        self.root.mainloop()


def main():
    print("Starting Autoclicker...")
    print("Press F6 to toggle autoclicking on/off")
    print("-" * 40)

    app = Autoclicker()
    app.run()


if __name__ == "__main__":
    main()
