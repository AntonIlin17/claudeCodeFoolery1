# Autoclicker

A simple, configurable autoclicker application with a graphical interface. Perfect for gaming, automation tasks, and accessibility needs.

## Features

- **Configurable click interval** - Set custom intervals from 10ms to any value
- **Multiple click buttons** - Left, right, or middle mouse button
- **Click types** - Single or double click
- **Position modes** - Click at cursor position or a fixed screen location
- **Hotkey support** - Press F6 to toggle on/off without touching the GUI
- **Real-time cursor tracking** - See current cursor position live

## Installation

### Requirements
- Python 3.7+
- tkinter (usually included with Python)

### Install Dependencies

```bash
pip install -r autoclicker_requirements.txt
```

### Linux Additional Setup
On Linux, you may need to install additional packages:

```bash
# For Debian/Ubuntu
sudo apt-get install python3-tk python3-dev

# You may also need to run with sudo for input simulation
sudo python3 autoclicker.py
```

### macOS Additional Setup
On macOS, you'll need to grant accessibility permissions to your terminal/Python.

Go to: **System Preferences > Security & Privacy > Privacy > Accessibility**

Add your terminal application (Terminal, iTerm2, etc.) to the list.

## Usage

### Running the App

```bash
python3 autoclicker.py
```

### Controls

1. **Click Interval**: Set how fast the clicks happen (in milliseconds)
   - Quick buttons: 50ms, 100ms, 250ms, 500ms, 1000ms
   - Or enter a custom value

2. **Click Button**: Choose which mouse button to simulate
   - Left Click (default)
   - Right Click
   - Middle Click

3. **Click Type**: Choose click behavior
   - Single Click
   - Double Click

4. **Click Position**: Where to click
   - Current Cursor Position: Clicks wherever your mouse is
   - Fixed Position: Clicks at specific X, Y coordinates
   - Use "Get Current Position" to capture your current mouse location

5. **Hotkey**: Press **F6** to start/stop clicking
   - Works even when the window is not focused
   - Great for gaming - start clicking without alt-tabbing

### Tips for Gaming

1. **Set your interval** based on game requirements (some games have anti-cheat)
2. **Use fixed position** for idle/clicker games where you need to click a specific spot
3. **Use F6 hotkey** to toggle without leaving your game
4. **Start with slower intervals** (250ms+) and adjust as needed

## Troubleshooting

### "Permission denied" on Linux
Run with sudo:
```bash
sudo python3 autoclicker.py
```

### Clicks not registering in games
- Some games block simulated input
- Try running the autoclicker as administrator
- Check if the game has anti-cheat that blocks automation

### GUI not appearing
Make sure tkinter is installed:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (via Homebrew)
brew install python-tk
```

## Disclaimer

Use this tool responsibly. Some games and applications prohibit the use of autoclickers and may ban accounts using them. Always check the terms of service before using automation tools in online games or services.
