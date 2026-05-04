import serial
import time
import numpy as np
 

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

    
    def write(self, command):
        """
        Send one command to the OC3.
        Example: oc.write("!jxx;1;")
        """
        self.ser.write((command + "\r").encode())  # Send command with carriage return
        self.ser.flush()  # Waits for all pending data to be sent
        time.sleep(0.3)

    def read(self):
        """
        Read the OC3 answer as clean text.
        """
        data = self.ser.read(512)  # Read up to 512 bytes
        return data.lstrip(b'\x01').strip()  # Remove leading \x01 and trailing whitespace

    def query(self, command):
        """
        Send command, then read answer.
        """
        self.write(command)
        return self.read()  # Return the OC3 answer as clean text

    # ---------- OC3 commands ----------

    def status(self):
        """
        Return the OC3 status as clean text.
        Example answer: b'!jxx;25.000;0;0;0;0;0;0;0;0;0;0'
        """
        return self.query("!jxx;1;")

    def enable(self):
        """
        Enable the OC3.
        """
        self.write("!mxx1;1;")

    def disable(self):
        """
        Disable the OC3.
        """
        self.write("!mxx0;0;")

    def set_temperature(self, temperature, ramp=100):
        """
        Set the OC3 temperature.
        """
        command = f"!ixx1;{temperature:.3f};100;0;{ramp:.3f};1;0;"
        self.write(command)

    def temperature(self):
        """
        Return actual measured temperature as float.
        """
        answer = self.status()
        return float(answer.decode().split(";")[1])

    def close(self):
        self.ser.close()
    
    # ----- Helper functions -----

    def get_mean_temperature(oc, duration_s=2.0):
        """
        Measure the mean temperature over a given duration.
        """
        t0 = time.time()
        values = []

        while True:
            now = time.time() - t0

            if now >= duration_s:
                break

            if now < duration_s:
                values.append(oc.temperature())

        values = np.array(values)

        mean_T = np.mean(values)
        std_T = np.std(values, ddof=1)
        err_T = std_T / np.sqrt(len(values))

        return mean_T, err_T