import numpy as np
import math
from Inverse_Kinematics import inverse_kinematics_m1_pro

# Define the joint ranges for M1-Pro
joint_ranges = {
    'joint_1': np.linspace(-180, 180, 20),  # Joint 1 range
    'joint_2': np.linspace(-90, 90, 30),    # Joint 2 range
    'joint_3': np.linspace(0, 100, 25),      # Joint 3 range (Prismatic)
    'joint_4': np.linspace(-180, 180, 40)   # Joint 4 range
}

# Function to read Cartesian coordinates from a file
def read_cartesian_coordinates(filename):
    cartesian_coords = []
    with open(filename, 'r') as file:
        for line in file:
            coords = list(map(float, line.strip().split(',')))
            cartesian_coords.append(coords)
    return cartesian_coords

# Define Q-learning parameters and actions (as done in previous scripts)
alpha = 0.1  # Learning rate
gamma = 0.95  # Discount factor
actions = [
    (-1, 0, 0, 0),  # Decrease joint 1
    (1, 0, 0, 0),   # Increase joint 1
    (0, -1, 0, 0),  # Decrease joint 2
    (0, 1, 0, 0),   # Increase joint 2
    (0, 0, -1, 0),  # Decrease joint 3 (Z-axis)
    (0, 0, 1, 0),   # Increase joint 3 (Z-axis)
    (0, 0, 0, -1),  # Decrease joint 4
    (0, 0, 0, 1),   # Increase joint 4
    (0, 0, 0, 0)    # No movement
]

# Initialize Q-table (make sure the dimensions are appropriate)
q_table = np.random.uniform(low=-1, high=1, size=(20, 30, 25, 40, len(actions)))

# Function to get discrete state (as done previously)
def get_discrete_state(joint_positions):
    state_indices = []
    for i, joint in enumerate(joint_positions):
        joint_name = f'joint_{i+1}'
        state_index = np.argmin(np.abs(joint_ranges[joint_name] - joint))
        state_indices.append(state_index)
    return tuple(state_indices)

def apply_action(joint_positions, action):
    """
    Applies the selected action to the current joint positions.

    Parameters:
    joint_positions (tuple): Current joint angles.
    action (tuple): Change to apply to the joint angles.

    Returns:
    new_joint_positions (tuple): Updated joint angles after applying action.
    """
    new_positions = [max(min(joint + delta, max_range), min_range)
                     for joint, (delta, min_range, max_range) in zip(joint_positions, 
                     [(action[0], -180, 180), (action[1], -90, 90), 
                      (action[2], 0, 100), (action[3], -180, 180)])]
    return tuple(new_positions)

# Update rule (as done previously)
def update_q_value(state, action, reward, new_state, alpha, gamma):
    current_q = q_table[state + (action,)]
    max_future_q = np.max(q_table[new_state])
    new_q = (1 - alpha) * current_q + alpha * (reward + gamma * max_future_q)
    q_table[state + (action,)] = new_q

# Main processing function
def process_cartesian_file(filename):
    L1 = 200.0  # length of the first link in mm (shoulder to first joint)
    L2 = 200.0  # length of the second link in mm (first to second joint)
    z_base = 5.0  # height of the robot base in mm
    theta4 = math.radians(30)  # desired orientation of the end-effector in radians
    cartesian_coords_list = read_cartesian_coordinates(filename)
    joint_coords_list = []
    for episode, cartesian_coords in enumerate(cartesian_coords_list):
        # Print current episode number
        print(f"\nEpisode {episode + 1}/{len(cartesian_coords_list)}")
        
        joint_positions = inverse_kinematics_m1_pro(cartesian_coords[0], cartesian_coords[1], cartesian_coords[2], L1, L2, z_base, theta4)
        # with open('joint_coordinates.txt', 'w') as f:
        #     f.write(f"{joint_positions[0]:.2f}, {joint_positions[1]:.2f}, {joint_positions[2]:.2f}, {joint_positions[3]:.2f}\n")
        joint_coords_list.append(joint_positions)
            
        state = get_discrete_state(joint_positions)
        
        print(f"Current State (Joint Positions): {joint_positions}")
        # Select a random action for demonstration (update this as needed)
        action = np.random.choice(len(actions))
        print(f"Selected Action: {actions[action]}")
        # Simulate a reward (you should implement your actual reward function)
        reward = np.random.uniform(-1, 1)
        print(f"Reward received: {reward}")
        
        # Apply the action to get new joint positions
        new_joint_positions = apply_action(joint_positions, actions[action])
        new_state = get_discrete_state(new_joint_positions)
        print(f"New State (Joint Positions): {new_joint_positions}")
        
        # Update the Q-value
        update_q_value(state, action, reward, new_state, alpha, gamma)
        print(f"Updated Q-value for State {state} and Action {action}: {q_table[state + (action,)]}")
    
    with open('joint_coordinates.txt', 'w') as f:
        for coords in joint_coords_list:
            f.write(f"{coords[0]:.2f}, {coords[1]:.2f}, {coords[2]:.2f}, {coords[3]:.2f}\n")

# Execute the processing
process_cartesian_file('cartesian_coordinates.txt')

print("Q-learning process completed with Cartesian coordinates.")
