import subprocess
import shutil
import os
import glob
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# test the points in k lattice from 1 1 1 to 9 9 9
with open('k-outputs.out', 'w') as f:
    f.write("k_point,total_energy\n")

#tests from 1 to 9 k points
for x in range(1, 9):
    #makes a copy of the diamond-scf.in file
    #modifies line 25 of the copy to change the k-points grid
    #runs pw.x to calculate the total energy
    #appends the cutoff energy and total energy to the k-outputs.out file
    commands = [
        f'cp diamond-scf.in k-in_{x}.in',
        f'sed -i -e "25s/.*/  {x} {x} {x}  1 1 1/" k-in_{x}.in',
        f'pw.x -input k-in_{x}.in > k-out_{x}.out',
        f'echo "{x}, $(grep -o \'!    total energy.*\' k-out_{x}.out | grep -o \'[-0-9.]*\')" >> k-outputs.out'
    ]
    for command in commands:
        subprocess.run(['/bin/bash', '-c', command])

# Move run-files to a directory
directory = 'k_points-run_files'
shutil.rmtree(directory, ignore_errors=True)
os.makedirs(directory, exist_ok=True)
for x in range(1, 9):
    shutil.move(f'k-in_{x}.in', directory, copy_function=shutil.copy2)
    shutil.move(f'k-out_{x}.out', directory, copy_function=shutil.copy2)
    files_to_delete = glob.glob(f'k-in_{x}.in-e')
    for file in files_to_delete:
        os.remove(file)

# Read the CSV file
data = pd.read_csv('~/Documents/shared/k-outputs.out')

# Extract the variables from the CSV columns
variable1 = data['k_point']
variable2 = data['total_energy']/2

# Calculate the difference between successive values of total system energy
diff_variable2 = -variable2.diff()

# Plot the variables
fig, ax1 = plt.subplots()

# Plot variable2 on the first axis
ax1.plot(variable1, variable2, color='blue')
ax1.set_xlabel('Number of K Points')
ax1.set_ylabel('Total System Energy (Ry)', color='blue')

# Create a second axis sharing the same x-axis
ax2 = ax1.twinx()

# Plot diff_variable2 on the second axis
ax2.plot(variable1, diff_variable2, color='red')
ax2.set_ylabel('Difference in Energy (Ry)', color='red')

# Add a horizontal line at 0.0007
ax2.axhline(y=0.0007, color='green', linestyle='--', label='Convergence Goal')

# Show the legend
ax2.legend()

# Print the first k-points and E_total of diff_variable2 below 0.0007
mask = diff_variable2 < 0.0007
first_below_threshold = diff_variable2[mask].iloc[0]
first_k_points_below_threshold = variable1[mask].iloc[0]
print("First k-points below 0.007:", first_k_points_below_threshold)
print("First E_total below 0.0007:", first_below_threshold)

# Show the plot
plt.show()
