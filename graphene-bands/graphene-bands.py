import numpy as np
import subprocess
import matplotlib.pyplot as plt

path = [
    [0.5, -0.5, 0, 20],      # M
    [0, 0, 0, 20],              # GAMMA
    [0.66666666, -0.33333333, 0, 20],   # K
    [0.5, -0.5, 0, 20]      # M
]
distances = []
for i in range(len(path) - 1):
    x1, y1, z1, _ = path[i]
    x2, y2, z2, _ = path[i + 1]
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5
    distances.append(distance)

normalized_distances = [int(40*(distance / max(distances))) for distance in distances]
normalized_distances[2] = 20
successive_distances_sum = [0] + [sum(normalized_distances[:i+1]) for i in range(len(distances))]
print(normalized_distances)

# Get scf calculation, save e-density to the tmp folder
pw_command = "pw.x < graphene-scf.in > graphene-scf.out"
subprocess.run(pw_command, shell=True)

# Run pw.x command to generate bands using previous scf
pw_command = "pw.x < graphene-band-make.in > graphene-band-make.out"
subprocess.run(pw_command, shell=True)

# Run bands.x command
bands_command = "bands.x < graphene-gnu.in > graphene-gnu.out"
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

markers = ['M','$\Gamma$','K','M']
# Add text and vertical lines for every 20 data points

for i in range(len(markers)):
    text_position = successive_distances_sum[i]
    text_label = markers[i]
    plt.text(text_position, -23.5, text_label, ha='center')
    plt.axvline(x=text_position, color='gray', linestyle='--')

plt.xticks([])  # Disable x-axis number markers
plt.xlim(0, max(successive_distances_sum))  # Set the x-axis limits

plt.show()
