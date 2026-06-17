from time import time, sleep
import numpy as np

def record_pm100a(ressource, duration_s=10.0, dt_s=0.1):
    """
    Record power meter readings for a specified duration and sampling interval.
    :param ressource: PyVISA instrument handle for the PM100A power meter
    :param duration_s: Total recording duration in seconds
    :param dt_s: Time interval between consecutive readings in seconds

    :return: Tuple of (mean power in mW, error on the mean in mW, values_mW)
    """
    t0 = time()

    times = []
    values_mW = []

    while time() - t0 < duration_s:
        t = time() - t0
        # Do not use READ? It is a different/older measurement path or stale low-level reading
        P_W = float(ressource.query("MEAS:POW?").strip())
        values_mW.append(P_W * 1e3)
        # print(value_mW)
        times.append(t)

        sleep(dt_s)

    times = np.array(times)
    values_mW = np.array(values_mW)

    mean_mW = np.mean(values_mW)
    std_mW = np.std(values_mW, ddof=1)
    error_mW = std_mW / np.sqrt(len(values_mW))  # error on the mean

    return mean_mW, error_mW, values_mW