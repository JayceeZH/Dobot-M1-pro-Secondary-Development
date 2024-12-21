import numpy as np

# Define the joint ranges for M1-Pro
joint_ranges = {
    'joint_1': (-56, 56),  # Joint 1 range
    'joint_2': (-120, 120),  # Joint 2 range
    'joint_3': (100, 240),  # Joint 3 range (Prismatic)
    'joint_4': (-360, 360)  # Joint 4 range
}

# Function to randomly generate joint positions within the defined ranges
def generate_random_joint_positions():
    joint_1 = np.random.uniform(joint_ranges['joint_1'][0], joint_ranges['joint_1'][1])
    joint_2 = np.random.uniform(joint_ranges['joint_2'][0], joint_ranges['joint_2'][1])
    joint_3 = np.random.uniform(joint_ranges['joint_3'][0], joint_ranges['joint_3'][1])
    joint_4 = np.random.uniform(joint_ranges['joint_4'][0], joint_ranges['joint_4'][1])
    
    return joint_1, joint_2, joint_3, joint_4

# Function to simulate normal robot arm movement (e.g., avoiding extremes)
def generate_normal_joint_positions():
    joint_1 = np.random.uniform(joint_ranges['joint_1'][0] + 10, joint_ranges['joint_1'][1] - 10)  # Avoid extreme positions
    joint_2 = np.random.uniform(joint_ranges['joint_2'][0] + 20, joint_ranges['joint_2'][1] - 20)  # Avoid extreme positions
    joint_3 = np.random.uniform(joint_ranges['joint_3'][0] + 10, joint_ranges['joint_3'][1] - 10)  # Avoid extreme positions
    joint_4 = np.random.uniform(joint_ranges['joint_4'][0] + 10, joint_ranges['joint_4'][1] - 10)  # Avoid extreme positions
    
    return joint_1, joint_2, joint_3, joint_4

# Function to write joint positions to a file
def write_joint_positions_to_file(filename, joint_positions):
    with open(filename, 'a') as f:  # 'a' mode to append to the file
        f.write(f"{joint_positions[0]:.2f}, {joint_positions[1]:.2f}, {joint_positions[2]:.2f}, {joint_positions[3]:.2f}\n")

# Main function to generate and save random joint positions
def generate_and_save_joint_positions(num_positions, filename):
    for _ in range(num_positions):
        # Generate normal joint positions
        joint_positions = generate_normal_joint_positions()
        
        # Write joint positions to the file
        write_joint_positions_to_file(filename, joint_positions)
        
        # Print generated joint positions for verification
        print(f"Generated Joint Positions: {joint_positions}")

# Generate and save 100 random joint positions
generate_and_save_joint_positions(150, 'joint_coordinates.txt')

print("Random joint positions generated and saved successfully.")
