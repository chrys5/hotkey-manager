import sys, os
from pathlib import Path
root_dir = Path(__file__).resolve().parent
sys.path.append(root_dir)

import keyboard, subprocess
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import psutil

from hotkeys import HOTKEYS

PID_FILE = "running/running.txt"
SCRIPT_PATH = os.path.realpath(sys.argv[0])
ICO_FILE = "keyboard_k_6868.ico"
running = True

# kill previous instance of this script
def kill_previous_instance():
    for proc in psutil.process_iter(attrs=['pid', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and len(cmdline) > 1 and 'python' in cmdline[0] and os.path.realpath(cmdline[1]) == SCRIPT_PATH and proc.pid != os.getpid():
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# -------------- main window ----------------
def main_window():
    root = tk.Tk()
    root.title("Keybinds Status")
    root.iconbitmap(ICO_FILE)

    label = tk.Label(root, text="Keybinds are active!", font=("Arial", 20))
    label.pack(padx=30, pady=20)

    label2 = tk.Label(root, text=f"Contents of hotkeys.py:", font=("Arial", 12))
    label2.pack(pady=5)

    text_box = ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Courier", 10))
    text_box.pack(pady=5)
    text_box.insert(tk.INSERT, open("hotkeys.py").read())

    label3 = tk.Label(root, text="Press Ctrl+Alt+Shift+W to open this window again.", font=("Arial", 12))
    label3.pack(pady=5)

    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=10)

    open_hotkeys_button = tk.Button(
        buttons_frame,
        text="Open hotkeys.py in VS Code",
        font=("Arial", 12),
        command=lambda: subprocess.call("code hotkeys.py", shell=True)  #assume VS Code is installed and in PATH
    )
    open_hotkeys_button.grid(row=0, column=0, padx=5)

    exit_button = tk.Button(
        buttons_frame,
        text="Exit and stop keybinds",
        font=("Arial", 12),
        command=lambda: close_app(root)
    )
    exit_button.grid(row=0, column=1, padx=5)

    root.mainloop()

def close_app(root: tk.Tk):
    root.destroy()
    exit_program()
# -------------------------------------------

def exit_program():
    global running
    running = False
    exit()

def main():
    kill_previous_instance()

    # write pid to file
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    for hotkey, function in HOTKEYS:
        keyboard.add_hotkey(hotkey, function)
    keyboard.add_hotkey("ctrl+alt+shift+w", main_window)
    running = True
    main_window()
    while running:
        keyboard.wait()
    exit()

if __name__ == "__main__":
    main()