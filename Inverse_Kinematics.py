import math

def inverse_kinematics_m1_pro(x, y, z, L1, L2, z_base, theta4):
    """
    Computes the joint angles (theta1, theta2) and the prismatic displacement (d3) for the M1-Pro SCARA robot.

    Parameters:
    x (float): x-coordinate of the end-effector
    y (float): y-coordinate of the end-effector
    z (float): z-coordinate of the end-effector
    L1 (float): length of the first link (shoulder to first joint)
    L2 (float): length of the second link (first to second joint)
    z_base (float): height of the base of the robot (initial z-coordinate)
    theta4 (float): desired orientation of the end-effector (in radians)

    Returns:
    (theta1, theta2, theta4, d3): Tuple of joint angles in radians and prismatic joint displacement
    """
    # Calculate the shoulder joint angle (theta1)
    theta1 = math.atan2(y, x)
    
    # Distance from shoulder to end-effector in the xy-plane
    r = math.sqrt(x**2 + y**2)
    
    # Check if the point is within the robot's reach
    if r > (L1 + L2) or r < abs(L1 - L2):
        raise ValueError("The point is outside the robot's reachable workspace.")
    
    # Elbow joint angle (theta2) using the law of cosines
    cos_theta2 = (r**2 - L1**2 - L2**2) / (2 * L1 * L2)
    # Handle the case where cos_theta2 is out of bounds
    if cos_theta2 < -1 or cos_theta2 > 1:
        raise ValueError("The calculated elbow angle is out of range.")
    
    theta2 = math.acos(cos_theta2)
    
    # Vertical prismatic joint displacement (d3)
    d3 = z_base - z

    return theta1, theta2, theta4, d3

# # Example usage
# x = 150.0  # x-coordinate of the end-effector in mm
# y = 100.0  # y-coordinate of the end-effector in mm
# z = 100.0  # z-coordinate of the end-effector in mm

# try:
#     theta1, theta2, theta4, d3 = inverse_kinematics_m1_pro(x, y, z, L1, L2, z_base, theta4)
#     print(f"Theta 1: {math.degrees(theta1):.2f} degrees")
#     print(f"Theta 2: {math.degrees(theta2):.2f} degrees")
#     print(f"Theta 4 (end-effector): {math.degrees(theta4):.2f} degrees")
#     print(f"Prismatic joint displacement d3: {d3:.2f} mm")
# except ValueError as e:
#     print(e)
