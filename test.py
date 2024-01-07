import os

subdirectories = ['diamond-bands', 'diamond-scf', 'graphene-bands', 'methane']

for subdir in subdirectories:
    path = os.path.join(os.getcwd(), subdir)
    os.chdir(path)  # Change directory to subdir
    if subdir == 'methane':
        os.system('pw.x < methane.in > methane.out')
    else:
        for file in os.listdir(path):
            if file.endswith('.py'):
                os.system(f'python3 {os.path.join(path, file)}')
    os.chdir('..')  # Change directory back to parent directory
