import numpy as np
import subprocess
import matplotlib.pyplot as plt

# Run self-consistient field for the diamond structure to get electron density
pw_command = "pw.x < diamond-scf.in > diamond-scf.out"
subprocess.run(pw_command, shell=True)

# Get the band energy levels for all the k-points defined in the diamond-band-make.in file
pw_command = "pw.x < diamond-band-make.in > diamond-band-make.out"
subprocess.run(pw_command, shell=True)

# Run bands.x command to output the bandsdata.gnu file
bands_command = "bands.x < diamond-gnu.in > diamond-gnu.out"
subprocess.run(bands_command, shell=True)

# Read the data from the file
data = []
series = []
with open("bandsdata.gnu", "r") as file:
    for line in file:
        if line.strip() == "":
            if series:
                data.append(np.array(series))
                series = []
        else:
            values = line.strip().split()
            k_vector = float(values[0])
            energy = float(values[1])
            series.append((k_vector, energy))

# Append the last series
if series:
    data.append(np.array(series))

# Plot the data
for series in data:
    k_vector, energy = zip(*series)
    plt.plot(range(len(k_vector)), energy)

#plt.xlabel("k-vector")
plt.ylabel("Energy (eV)")
plt.title("Diamond Band Structure")

markers = ['W', 'L', '\u03B3', 'X', 'W', 'K']
# Add text and vertical lines for every 20 data points
for i in range(6):
    text_position = 20*i
    text_label = markers[i]
    plt.text(text_position, -13, text_label, ha='center')
    plt.axvline(x=text_position, color='gray', linestyle='--')

plt.xticks([])

plt.show()
