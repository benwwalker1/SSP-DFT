import numpy as np
import subprocess
import matplotlib.pyplot as plt

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
    count = int(np.floor(len(k_vector)/20))

#plt.xlabel("k-vector")
plt.ylabel("Energy (eV)")
plt.title("Data Plot")

markers = ['K','\u03B3','M','K']
# Add text and vertical lines for every 20 data points

for i in range(count+1):
    text_position = 20*i
    text_label = markers[i]
    plt.text(text_position, -23.5, text_label, ha='center')
    plt.axvline(x=text_position, color='gray', linestyle='--')

plt.xticks([])  # Disable x-axis number markers

plt.show()
