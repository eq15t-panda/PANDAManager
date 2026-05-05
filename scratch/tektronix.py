import os
import time
import struct
import numpy as np

from .scpi import scpi_write, scpi_readline, read_block

def get_channel_display_state(fd, channel: str) -> bool:
    scpi_write(fd, f"SEL:{channel}?")
    ans = scpi_readline(fd)
    return ans.strip() in ("1", "ON")

def setup_waveform_transfer(fd, channel: str) -> None:
    '''
    Configure waveform transfer for one channel.
    This is intentionally intrusive and only meant for the Tektronix acquisition section.
    '''
    scpi_write(fd, f"DATA:SOURCE {channel}")
    scpi_write(fd, "DATA:ENC RIBINARY")
    scpi_write(fd, "DATA:WIDTH 2")
    scpi_write(fd, "DATA:START 1")
    scpi_write(fd, "DATA:STOP 1000000")
    time.sleep(0.05)

def read_waveform_preamble(fd) -> dict:
    scpi_write(fd, "WFMOutpre?")
    preamble = scpi_readline(fd)
    fields = preamble.split(";")
    return {
        "xincr": float(fields[9]),
        "xzero": float(fields[10]),
        "ymult": float(fields[13]),
        "yzero": float(fields[14]),
        "yoff": float(fields[15]),
        "xunit": fields[11].strip('"'),
        "yunit": fields[12].strip('"'),
        "raw_preamble": preamble,
    }

def read_waveform_binary(fd) -> tuple[np.ndarray, np.ndarray]:
    meta = read_waveform_preamble(fd)
    scpi_write(fd, "CURVE?")
    raw = read_block(fd)
    n_pts = len(raw) // 2
    adc = np.array(struct.unpack(f">{n_pts}h", raw), dtype=np.int16)
    volts = (adc - meta["yoff"]) * meta["ymult"] + meta["yzero"]
    time_axis = meta["xzero"] + np.arange(n_pts) * meta["xincr"]
    return time_axis, volts, meta

def acquire_displayed_channels(fd, channels, only_displayed=True):
    all_data = {}
    saved_channels = []
    for ch in channels:
        if only_displayed and not get_channel_display_state(fd, ch):
            print(f"{ch}: not displayed, skipped")
            continue

        setup_waveform_transfer(fd, ch)
        t, v, meta = read_waveform_binary(fd)
        all_data[f"{ch}_time"] = t
        all_data[f"{ch}_volts"] = v
        all_data[f"{ch}_meta"] = meta
        saved_channels.append(ch)
        print(f"{ch}: acquired {len(v)} points")
    all_data["saved_channels"] = saved_channels
    return all_data
