import subprocess
import shutil
import os
import glob
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#intitialize the outputs file
with open('lattice_outputs.out', 'w') as f:
    f.write("lattice_const,energy\n")

# test the lattice parameter from 6.41 to 7.09 in steps of 0.01 rydberg
lower_limit = 6.41
num_steps = 68
step = 0.01
for i in range(num_steps + 1):
    x = lower_limit + (step * i)
    x = round(x, 2)
    #makes a copy of the diamond-scf.in file
    #modifies line 10 of the copy to change the lattice constant
    #runs pw.x to calculate the total energy
    #appends the lattice const and total energy to the lattice_outputs.out file
    commands = [
        f'cp diamond-scf.in lattice-in_{x}.in',
        f'sed -i -e "10s/.*/  celldm(1) = {x},/" lattice-in_{x}.in',
        f'pw.x -input lattice-in_{x}.in > lattice-out_{x}.out',
        f'echo "{x}, $(grep -o \'!    total energy.*\' lattice-out_{x}.out | grep -o \'[-0-9.]*\')" >> lattice_outputs.out'
    ]
    for command in commands:
        subprocess.run(['/bin/bash', '-c', command])

# Move files to a directory
directory = 'lattice-run_files'
shutil.rmtree(directory, ignore_errors=True)
os.makedirs(directory, exist_ok=True)
for i in range(num_steps + 1):
    x = lower_limit + (step * i)
    x = round(x, 2)

    shutil.move(f'lattice-in_{x}.in', directory, copy_function=shutil.copy2)
    shutil.move(f'lattice-out_{x}.out', directory, copy_function=shutil.copy2)
    files_to_delete = glob.glob(f'lattice-in_{x}.in-e')
    for file in files_to_delete:
        os.remove(file)


#read the outputs file
lattice_data = pd.read_csv('lattice_outputs.out')

# Extract the variables from the CSV columns
volume = (lattice_data['lattice_const']**3)/4 #converts lattice const to volume of cell
energy = lattice_data['energy']

# Fit a 4th degree polynomial
coefficients = np.polyfit(volume, energy, 4)
polynomial = np.poly1d(coefficients)

# Plot the variables
plt.plot(volume, energy, label='Data')
plt.plot(volume, polynomial(volume), label='Best Fit')

# Add axes labels
plt.xlabel('Cell Volume (Bohr^3)')
plt.ylabel('Energy (Ry))')

# Find the minimum value and its corresponding lattice constant
min_index = np.argmin(energy)
min_value = energy[min_index]
min_volume = volume[min_index]

# Take the second derivative of the polynomial at the minimum volume
second_derivative = np.polyder(np.polyder(polynomial))(min_volume)

#calculate the bulk modulus in GPa
bulk_mod = min_volume * second_derivative * 1.47e13 / 1e9

print(f"Cell Volume: {min_volume} Bohr^3")
print(f"Lattice Parameter: {(4*min_volume)**(1/3)} Bohr^3")
print(f"Second Derivative at Minimum Volume: {second_derivative}")
print(f"Bulk Modulus: {bulk_mod} GPa")

# Show the legend
plt.legend()

# Show the plot
plt.show()