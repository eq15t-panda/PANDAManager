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


def read_powers_and_temp(
    port='COM4',
    harmonik_addr=74,
):
    openPorts(port, 0, 0)

    try:
        # Harmonik input power
        _, in_bytes = registerRead(port, harmonik_addr, 0x91, -1)
        harmonik_input = struct.unpack('<f', in_bytes[:4])[0]

        # Harmonik output power
        _, out_bytes = registerRead(port, harmonik_addr, 0x9D, -1)
        harmonik_output = struct.unpack('<f', out_bytes[:4])[0]

        # Harmonik temperature
        _, temp_bytes = registerRead(port, harmonik_addr, 0xBA, -1)
        harmonik_temp = struct.unpack('<f', temp_bytes[:4])[0]

    finally:
        closePorts(port)

    return harmonik_input, harmonik_output, harmonik_temp