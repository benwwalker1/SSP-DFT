import subprocess
import shutil
import os
import glob
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# test the cutoff energy from 40 to 115 Ry in steps of 5 Ry
with open('e-cutoff.out', 'w') as f:
    f.write("E_cutoff,E_total\n")

#tests from ecuttof of 40 to 120 in steps of 5 rydberg
for x in range(40, 120, 5):
    #makes a copy of the diamond-scf.in file
    #modifies line 13 of the copy to change the cutoff energy
    #runs pw.x to calculate the total energy
    #appends the cutoff energy and total energy to the e-cutoff.out file
    commands = [
        f'cp diamond-scf.in e-in_{x}.in',
        f'sed -i -e "13s/.*/  ecutwfc = {x},/" e-in_{x}.in',
        f'pw.x < e-in_{x}.in > e-out_{x}.out',
        f'echo "{x}, $(grep -o \'!    total energy.*\' e-out_{x}.out | grep -o \'[-0-9.]*\')" >> e-cutoff.out'
    ]
    for command in commands:
        subprocess.run(['/bin/bash', '-c', command])

# Move all run-files to a directory
        
directory = 'e_cutoff-run_files'
shutil.rmtree(directory, ignore_errors=True)
os.makedirs(directory, exist_ok=True)

for x in range(40, 120, 5):
    shutil.move(f'e-in_{x}.in', directory, copy_function=shutil.copy2)
    shutil.move(f'e-out_{x}.out', directory, copy_function=shutil.copy2)
    files_to_delete = glob.glob(f'e-in_{x}.in-e') #deletes weird files that shouldn't exist
    for file in files_to_delete:
        os.remove(file)

# Read the CSV file
data = pd.read_csv('e-cutoff.out')

# Extract the variables from the CSV columns
variable1 = data['E_cutoff']
variable2 = data['E_total']/2 # Divide by 2 to get the energy per atom

# Calculate the difference between successive values of total system energy
diff_variable2 = -variable2.diff()

# Create a new figure and axis
fig, ax1 = plt.subplots()

# Plot variable2 on the first axis
ax1.plot(variable1, variable2, color='blue')
ax1.set_xlabel('Cutoff Energy (Ry)')
ax1.set_ylabel('Total System Energy (Ry)', color='blue')

# Create a second axis sharing the same x-axis
ax2 = ax1.twinx()

# Plot diff_variable2 on the second axis
ax2.plot(variable1, diff_variable2, color='red')
ax2.set_ylabel('Difference in Energy (Ry)', color='red')

# Add a horizontal line at 0.007
ax2.axhline(y=0.0007, color='green', linestyle='--', label='Convergence Goal')

# Show the legend
ax2.legend()

# Print the first E_cutoff and E_total of diff_variable2 below 0.007
mask = diff_variable2 < 0.0007
first_below_threshold = diff_variable2[mask].iloc[0]
print("First E_cutoff below 0.007:", variable1[mask].iloc[0])
print("First E_total below 0.007:", first_below_threshold)

# Show the plot
plt.show()