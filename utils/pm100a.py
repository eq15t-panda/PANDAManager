import time
import numpy as np

from .scpi import scpi_write, scpi_readline


def pm_query(fd, cmd):
    scpi_write(fd, cmd)
    return scpi_readline(fd)

def pm_write_only(fd, cmd):
    scpi_write(fd, cmd)


def find_pm100a():
    import os
    import glob

    candidates = sorted(glob.glob("/dev/usbtmc*"))
    if not candidates:
        raise RuntimeError("No /dev/usbtmc* devices found")

    for dev in candidates:
        fd = None
        try:
            fd = os.open(dev, os.O_RDWR)
            time.sleep(0.1)
            idn = pm_query(fd, "*IDN?")
            print(f"{dev} -> {idn}")

            if "THORLABS" in idn.upper() and "PM100A" in idn.upper():
                return fd, dev, idn

            os.close(fd)
            fd = None

        except Exception as e:
            print(f"{dev} -> failed: {e}")
            if fd is not None:
                try:
                    os.close(fd)
                except Exception:
                    pass

    raise RuntimeError("PM100A not found")


def pm100a_get_sensor_info(fd):
    return pm_query(fd, "SYST:SENS:IDN?")


def pm100a_read_value(fd):
    return float(pm_query(fd, "READ?"))


def pm100a_fetch_value(fd):
    return float(pm_query(fd, "FETCh?"))


def pm100a_set_average_count(fd, count):
    pm_write_only(fd, f"SENSE:AVERAGE:COUNT {int(count)}")
    return int(pm_query(fd, "SENSE:AVERAGE:COUNT?"))


def pm100a_record_timeseries(fd, duration_s=10.0, sample_delay_s=0.1, use_fetch=False):
    """
    Record PM100A values over time for duration_s.
    Returns:
        t_rel : np.ndarray
        values : np.ndarray
    """
    t0 = time.time()
    times = []
    values = []

    read_fn = pm100a_fetch_value if use_fetch else pm100a_read_value

    while True:
        now = time.time()
        t_rel = now - t0
        if t_rel > duration_s:
            break

        val = read_fn(fd)
        times.append(t_rel)
        values.append(val)

        time.sleep(sample_delay_s)

    return np.array(times, dtype=float), np.array(values, dtype=float)