import time
import tkinter as tk

def generate_temperature_list(start, end, step):
    if step <= 0:
        raise ValueError("TEMP_STEP must be > 0")

    temps = []
    if end >= start:
        t = start
        while t <= end + 1e-12:
            temps.append(round(t, 10))
            t += step
    else:
        t = start
        while t >= end - 1e-12:
            temps.append(round(t, 10))
            t -= step
    return temps


def prompt_user_locked(message="Signal Locked, proceed? [Y/n] "):
    while True:
        ans = input(message).strip().lower()
        if ans in ("", "y", "yes"):
            return
        print("Waiting for lock confirmation...")


def wait_for_user_popup(message="Signal locked. Proceed to next point"):
    """
    Blocking popup with a single button.
    Execution resumes only when the user clicks.
    """

    root = tk.Tk()
    root.title("Acquisition control")

    # Make window appear on top
    root.attributes("-topmost", True)

    # Optional: fixed size
    root.geometry("320x120")

    label = tk.Label(root, text=message, font=("Arial", 12))
    label.pack(pady=20)

    def on_click():
        root.destroy()

    button = tk.Button(root, text="Proceed to next point", command=on_click)
    button.pack(pady=10)

    # Block here until window is closed
    root.mainloop()