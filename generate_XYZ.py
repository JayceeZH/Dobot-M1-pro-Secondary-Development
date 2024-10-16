import numpy as np

# Define the number of Cartesian coordinates to generate
num_coordinates = 100

# Define limits based on the M1-Pro's workspace
x_limits = (-200, 200)
y_limits = (-200, 200)
z_limits = (5, 245) # in unit of mm
rotation_limits = (0, 360) #range of end effector rotation degree

# Generate random Cartesian coordinates
cartesian_coords = []
for _ in range(num_coordinates):
    x = np.random.uniform(*x_limits)
    y = np.random.uniform(*y_limits)
    z = np.random.uniform(*z_limits)
    rotation = np.random.uniform(*rotation_limits)
    cartesian_coords.append((x, y, z, rotation))

# Write the coordinates to a .txt file
with open('cartesian_coordinates.txt', 'w') as f:
    for coords in cartesian_coords:
        f.write(f"{coords[0]:.2f}, {coords[1]:.2f}, {coords[2]:.2f}, {coords[3]:.2f}\n")

print("Random Cartesian coordinates saved to 'cartesian_coordinates.txt'")

