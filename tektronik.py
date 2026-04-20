import numpy as np
import matplotlib.pyplot as plt

filename = "data/T0015ALL.CSV"

# find the line where the actual CSV starts
with open(filename) as f:
    for i, line in enumerate(f):
        if line.startswith("TIME"):
            header_line = i
            break

# load the numeric data
data = np.loadtxt(filename, delimiter=",", skiprows=header_line + 1)

# columns
t = data[:,0]
ch1 = data[:,1]
ch2 = data[:,3]
ch4 = data[:,5]

# plot
plt.figure(figsize=(10,5))
plt.plot(t, ch1, label="CH1: Error signal")
plt.plot(t, ch2, label="CH2: PZT ramp")
plt.plot(t, ch4, label="CH4: Lock diode")

plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()