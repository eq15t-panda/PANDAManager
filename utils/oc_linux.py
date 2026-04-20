import serial
import time

class OC3:
    def __init__(self, port):
        self.ser = serial.Serial(
            port=port,
            baudrate=19200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
        time.sleep(0.3)
        self.ser.reset_input_buffer()

    def send(self, cmd: bytes):
        self.ser.write(cmd + b"\r")
        self.ser.flush()
        time.sleep(0.3)

    def read(self):
        data = self.ser.read(512)
        return data.lstrip(b'\x01').strip()

    # ---- COMMANDS ----

    def get_status(self):
        self.send(b"!jxx;1;")
        return self.read()

    def enable(self):
        self.send(b"!mxx1;1;")

    def disable(self):
        self.send(b"!mxx0;0;")

    def set_temperature(self, temp, ramp=100):
        cmd = f"!ixx1;{temp:.3f};100;0;{ramp:.3f};1;0;"
        self.send(cmd.encode())

    def close(self):
        self.ser.close()