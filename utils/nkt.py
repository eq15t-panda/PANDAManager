import struct
from sys import path
path.append(r"D:/NKT Photonics/Examples/DLL_Example_Python")

from NKTP_DLL import *


def find_nkt_devices(close_after=True):
    """
    Scan for NKT devices and return a list of open ports.

    Parameters
    ----------
    close_after : bool
        Close ports before returning.
    verbose : bool
        Print status messages.

    Returns
    -------
    list
        List of detected/open ports.
    """
    ports = getAllPorts()
    print("Scanning:", ports)

    result = openPorts(ports, 1, 1)
    print("Open result:", PortResultTypes(result))

    open_ports = getOpenPorts()
    if open_ports:
        print("Device(s) found on:", open_ports)
    else:
        print("No NKT devices found")

    if close_after:
        closePorts('')

    return open_ports


def read_power_and_temp(port='COM4', harmonik_addr=74, adjustik_addr=128):
    """Read power (W) and temperature (°C) from NKT modules."""
    openPorts(port, 0, 0)  # Open port

    # Read power (Harmonik-GW, register 0x9D, float32)
    _, power_bytes = registerRead(port, harmonik_addr, 0x9D, -1)
    power = struct.unpack('f', power_bytes[:4])[0]  # Ensure 4 bytes for float32

    # Read temperature (Adjustik, register 0x11, I16 in m°C)
    _, temp_bytes = registerRead(port, adjustik_addr, 0x11, -1)
    temp = struct.unpack('h', temp_bytes[:2])[0] / 1000  # Ensure 2 bytes for I16

    closePorts(port)  # Close port
    return power, temp