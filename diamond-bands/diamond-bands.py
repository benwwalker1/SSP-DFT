import numpy as np
import subprocess
import matplotlib.pyplot as plt


path = [
    [0.25, 0.5, -0.25, 20],    # W
    [0, 0.5, 0, 20],            # L
    [0, 0, 0, 20],              # GAMMA
    [0, -0.5, -0.5, 20],        # X
    [-0.25, -0.5, -0.75, 20],   # W
    [-0.375, -0.375, -0.75, 20] # K
]

distances = []
for i in range(len(path) - 1):
    x1, y1, z1, _ = path[i]
    x2, y2, z2, _ = path[i + 1]
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5
    distances.append(distance)

normalized_distances = [int(30*(distance / max(distances))) for distance in distances]
successive_distances_sum = [0] + [sum(normalized_distances[:i+1]) for i in range(len(distances))]
markers = ['W', 'L', '\u03B3', 'X','W', 'K']

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
    energy = [e-13.2908 for e in energy]   
    plt.plot(range(len(k_vector)), energy)
    print(successive_distances_sum[2],energy[successive_distances_sum[2]])
    print(successive_distances_sum[3],energy[successive_distances_sum[3]])

k_vector, c_energy = zip(*data[4])
k_vector, c2_energy = zip(*data[5])
k_vector, v_energy = zip(*data[3])
indirect_bandgap = min(abs(min(c2_energy)-max(v_energy)),abs(min(c_energy-max(v_energy))))
print("Indirect Bandgap:", indirect_bandgap)
direct_bandgap = c_energy[successive_distances_sum[2]]-v_energy[successive_distances_sum[2]]
print("Direct Bandgap:", direct_bandgap)
#plt.xlabel("k-vector")
plt.ylabel("Energy (eV)")

# Add text and vertical lines for every data point
for i in range(len(markers)):
    text_position = successive_distances_sum[i]
    text_label = markers[i]
    plt.text(text_position, -26.3, text_label, ha='center')
    plt.axvline(x=text_position, color='gray', linestyle='--')

plt.xticks([])
plt.xlim(0, max(successive_distances_sum))  # Set the x-axis limits

plt.show()


