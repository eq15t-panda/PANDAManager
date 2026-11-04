"""
utils/oscilloscope.py

Unified oscilloscope interface for Tektronix and Agilent/Keysight scopes.
Detects the brand from the IDN string and dispatches the right SCPI commands.

Supported:
  - Tektronix  (IDN contains "TEKTRONIX")
  - Agilent / Keysight  (IDN contains "AGILENT" or "KEYSIGHT")
"""

import numpy as np


# Brand detection
def get_brand(scope) -> str:
    """
    Identify the oscilloscope brand from its *IDN? response.

    :param scope: pyvisa resource (already open)
    :return: "tektronix" | "agilent" | raises ValueError if unknown
    """
    idn = scope.query("*IDN?").strip().upper()

    if "TEKTRONIX" in idn:
        return "tektronix"
    if "AGILENT" in idn or "KEYSIGHT" in idn:
        return "agilent"

    raise ValueError(f"Unknown oscilloscope brand. IDN string: {idn}. Add support for this brand in utils/oscilloscope.py -> get_brand.")


# Active channel detection
def get_active_channels(scope, brand: str) -> list[str]:
    """
    Return a list of channel names that are currently displayed on screen.

    :param scope: pyvisa resource (already open)
    :param brand: "tektronix" or "agilent"
    :return: list of active channel strings, e.g. ["CH1", "CH3"]
    """
    channels = ["CH1", "CH2", "CH3", "CH4"]

    if brand == "tektronix":
        # SEL? returns "1;0;1;0" style — one flag per channel
        sel = scope.query("SEL?").strip().split(";")
        return [ch for ch, flag in zip(channels, sel) if flag == "1"]

    if brand == "agilent":
        # Query each channel display state individually with :CHAN:DISP?
        active = []
        for ch in channels:
            ch_num = ch.replace("CH", "")                # "CH1" → "1"
            state = scope.query(f":CHAN{ch_num}:DISP?").strip()
            if state == "1":
                active.append(ch)
        return active

    raise ValueError(f"Unsupported brand: {brand}")


# Waveform acquisition
def acquire_waveform(scope, brand: str, channel: str) -> dict:
    """
    Retrieve the waveform (x, y) and all scaling metadata for one channel.

    :param scope: pyvisa resource (already open, acquisition stopped)
    :param brand: "tektronix" or "agilent"
    :param channel: channel string, e.g. "CH1"
    :return: dict with keys x, y, y_raw, ymult, yoff, yzero, xincr, xzero, pt_off
    """
    if brand == "tektronix":
        return _acquire_tektronix(scope, channel)

    if brand == "agilent":
        return _acquire_agilent(scope, channel)

    raise ValueError(f"Unsupported brand: {brand}")


def _acquire_tektronix(scope, channel: str) -> dict:
    """
    Tektronix waveform acquisition using WFMPRE preamble and CURVE binary transfer.

    :param scope: pyvisa resource
    :param channel: e.g. "CH1"
    :return: waveform data dict
    """
    scope.write(f"DATA:SOURCE {channel}")
    scope.write("DATA:ENC RIBINARY")  # signed binary
    scope.write("DATA:WIDTH 1")       # 1 byte per sample

    y_raw = scope.query_binary_values("CURVE?", datatype="b", container=np.array)

    ymult  = float(scope.query("WFMPRE:YMULT?"))
    yoff   = float(scope.query("WFMPRE:YOFF?"))
    yzero  = float(scope.query("WFMPRE:YZERO?"))
    xincr  = float(scope.query("WFMPRE:XINCR?"))
    xzero  = float(scope.query("WFMPRE:XZERO?"))
    pt_off = float(scope.query("WFMPRE:PT_OFF?"))

    y = (y_raw - yoff) * ymult + yzero
    x = xzero + (np.arange(len(y)) - pt_off) * xincr

    return dict(x=x, y=y, y_raw=y_raw,
                ymult=ymult, yoff=yoff, yzero=yzero,
                xincr=xincr, xzero=xzero, pt_off=pt_off)


def _acquire_agilent(scope, channel: str) -> dict:
    """
    Agilent/Keysight waveform acquisition using :WAV:PRE? preamble and :WAV:DATA? binary transfer.
    Preamble indices follow the InfiniiVision programmer's guide.

    :param scope: pyvisa resource
    :param channel: e.g. "CH1"
    :return: waveform data dict (same keys as Tektronix for consistency)
    """
    ch_num = channel.replace("CH", "")  # "CH1" → "1"

    scope.write(f":WAV:SOUR CHAN{ch_num}")
    scope.write(":WAV:FORM BYTE")        # unsigned 8-bit samples
    scope.write(":WAV:POIN:MODE NORM")   # normal (all displayed points)

    # Preamble: comma-separated list of 10 fields
    # [0] format, [1] type, [2] points, [3] count,
    # [4] xincr, [5] xorigin, [6] xref,
    # [7] yincr, [8] yorigin, [9] yref
    preamble = scope.query(":WAV:PRE?").strip().split(",")

    xincr  = float(preamble[4])
    xzero  = float(preamble[5])   # x origin (time of first sample)
    xref   = float(preamble[6])   # x reference (always 0)
    ymult  = float(preamble[7])   # y increment (volts per count)
    yzero  = float(preamble[8])   # y origin (voltage at y_ref)
    yref   = float(preamble[9])   # y reference (count at 0 V)

    y_raw = scope.query_binary_values(":WAV:DATA?", datatype="B", container=np.array)

    # Match Tektronix naming convention for downstream consistency
    yoff   = yref    # "offset" count plays the same role as Tek's YOFF
    pt_off = xref    # reference point index (always 0 for Agilent)

    y = (y_raw - yoff) * ymult + yzero
    x = xzero + (np.arange(len(y)) - pt_off) * xincr

    return dict(x=x, y=y, y_raw=y_raw,
                ymult=ymult, yoff=yoff, yzero=yzero,
                xincr=xincr, xzero=xzero, pt_off=pt_off)


# Acquisition run/stop

def stop_acquisition(scope, brand: str) -> None:
    """
    Freeze the scope display so waveforms are stable during readout.

    :param scope: pyvisa resource
    :param brand: "tektronix" or "agilent"
    :return: None
    """
    if brand == "tektronix":
        scope.write("ACQ:STATE STOP")
    elif brand == "agilent":
        scope.write(":STOP")
    else:
        raise ValueError(f"Unsupported brand: {brand}")


def run_acquisition(scope, brand: str) -> None:
    """
    Resume continuous acquisition after readout is complete.

    :param scope: pyvisa resource
    :param brand: "tektronix" or "agilent"
    :return: None
    """
    if brand == "tektronix":
        scope.write("ACQ:STATE RUN")
    elif brand == "agilent":
        scope.write(":RUN")
    else:
        raise ValueError(f"Unsupported brand: {brand}")


# Screenshot

def save_screenshot(scope, brand: str, filepath) -> None:
    """
    Capture a PNG screenshot from the oscilloscope screen and write it to disk.

    :param scope: pyvisa resource
    :param brand: "tektronix" or "agilent"
    :param filepath: pathlib.Path or str — destination file (should end in .png)
    :return: None
    """
    from pathlib import Path
    filepath = Path(filepath)

    if brand == "tektronix":
        scope.write("SAVe:IMAGe:FILEFormat PNG")
        scope.write("HARDCopy STARt")
        img_data = scope.read_raw()

    elif brand == "agilent":
        scope.write(":HCOP:SDUMP:DATA:FORM PNG")  # select PNG format
        scope.write(":HCOP:SDUMP:DATA?")          # request the image
        img_data = scope.read_raw()

    else:
        raise ValueError(f"Unsupported brand: {brand}")

    filepath.write_bytes(img_data)
    print(f"Screenshot saved → {filepath}")