import numpy as np

# Function to calculate the rotation matrix for a 3D rotation around the z-axis
def rotation_matrix_z(theta):
    cos_theta = np.cos(np.radians(theta))
    sin_theta = np.sin(np.radians(theta))
    return np.array([
        [cos_theta, -sin_theta, 0],
        [sin_theta, cos_theta, 0],
        [0, 0, 1]
    ])

# Function to calculate the rotation matrix for a 3D rotation around the x-axis
def rotation_matrix_x(theta):
    cos_theta = np.cos(np.radians(theta))
    sin_theta = np.sin(np.radians(theta))
    return np.array([
        [1, 0, 0],
        [0, cos_theta, -sin_theta],
        [0, sin_theta, cos_theta]
    ])

# assume initial hydrogren points in +z direction, use unit vector
vector_first = np.array([0, 0, 1])

# let the second vector rotate by 109.5 degrees around the x-axis, as predicted by theory
matrix1 = rotation_matrix_x(109.5)
vector_second = np.dot(matrix1, vector_first)

#looking down -z, all three vectors must be 120 degrees apart
matrix2 = rotation_matrix_z(120)
matrix3 = rotation_matrix_z(-120)
vector_third = np.dot(matrix2, vector_second)
vector_fourth = np.dot(matrix3, vector_second)

# Display results, multiply by the bond distance 1.09 angstrom
print("First Hydrogen Atom:", 1.09*vector_first)
print("Second Hydrogen Atom:", 1.09*vector_second)
print("Third Hydrogen Atom:", 1.09*vector_third)
print("Fourth Hydrogen Atom:", 1.09*vector_fourth)