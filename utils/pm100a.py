from time import time, sleep
import numpy as np

def record_pm100a(ressource, duration_s=10.0, dt_s=0.1):
    """
    Record power meter readings for a specified duration and sampling interval.
    :param ressource: PyVISA instrument handle for the PM100A power meter
    :param duration_s: Total recording duration in seconds
    :param dt_s: Time interval between consecutive readings in seconds

    :return: Tuple of (mean power in mW, error on the mean in mW)
    """
    t0 = time()

    times = []
    values_mW = []

    while time() - t0 < duration_s:
        t = time() - t0
        raw_value = ressource.query("READ?")  # Get raw reading from the instrument
        # print(raw_value)
        value_mW = float(raw_value[:-1]) * 1e3  # Convert from W to mW (assuming raw_value ends with 'W')
        # print(value_mW)
        times.append(t)
        values_mW.append(value_mW)

        sleep(dt_s)

    times = np.array(times)
    values_mW = np.array(values_mW)

    mean_mW = np.mean(values_mW)
    std_mW = np.std(values_mW, ddof=1)
    error_mW = std_mW / np.sqrt(len(values_mW))  # error on the mean

    return mean_mW, error_mW