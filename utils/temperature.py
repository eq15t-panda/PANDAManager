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

def get_oc3_temperature(oc):
    status = oc.get_status().decode()
    fields = status.split(";")
    return float(fields[1])

def wait_for_stable_temperature(oc, setpoint, tol, stable_time, poll_interval=1.0):
    t_stable = None
    while True:
        actual = get_oc3_temperature(oc)
        delta = abs(actual - setpoint)
        print(f"  T = {actual:.3f} °C | Δ = {delta:.3f} °C", end="\r")

        if delta < tol:
            if t_stable is None:
                t_stable = time.time()
            elif time.time() - t_stable >= stable_time:
                print()
                return actual
        else:
            t_stable = None

        time.sleep(poll_interval)

def prompt_user_locked(message="Signal Locked, proceed? [Y/n] "):
    while True:
        ans = input(message).strip().lower()
        if ans in ("", "y", "yes"):
            return
        print("Waiting for lock confirmation...")


def finalize_oc3(oc, start_temp, ramp_rate, wait_fn,
                 return_to_start=True,
                 keep_enabled=True,
                 close_connection=False):
    if oc is None:
        return

    if return_to_start:
        print(f"\nReturning controller to start temperature: {start_temp:.3f} °C")
        oc.set_temperature(start_temp, ramp=ramp_rate)
        time.sleep(0.5)
        T_back = wait_fn(oc, start_temp)
        print(f"Controller stabilized back at {T_back:.3f} °C")

    if keep_enabled:
        print("Keeping OC3 enabled.")
    else:
        oc.disable()
        print("OC3 disabled.")

    if close_connection:
        oc.close()
        print("OC3 connection closed.")


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