import serial
import time

# Configure the serial port (replace 'COM3' with the correct port for your system)
ser = serial.Serial('COM3', baudrate=115200, timeout=1)  # Adjust baudrate based on servo specifications

def send_command(command_bytes):
    """
    Sends a command to the servo.

    Parameters:
    command_bytes (bytes): The command as a byte array.
    """
    ser.write(command_bytes)
    time.sleep(0.1)  # Allow some time for the servo to process

def set_servo_angle(id, angle):
    """
    Set the servo to a specific angle.

    Parameters:
    id (int): Servo ID (if multiple servos are connected).
    angle (int): Target angle (e.g., 0-240 degrees).
    """
    if not (0 <= angle <= 240):
        print("Error: Angle must be between 0 and 240 degrees.")
        return
    
    # Example command structure (check your servo's documentation):
    # Command: [Header, ID, Command Type, Angle LSB, Angle MSB, Checksum]
    angle_low = angle & 0xFF
    angle_high = (angle >> 8) & 0xFF
    checksum = (id + 0x03 + angle_low + angle_high) & 0xFF  # Replace 0x03 with your command type
    command = bytes([0x55, 0x55, id, 0x03, angle_low, angle_high, checksum])
    
    send_command(command)

try:
    servo_id = 1  # Replace with your servo's ID
    
    # Example: Move servo back and forth
    while True:
        for angle in range(0, 241, 10):  # Move up
            set_servo_angle(servo_id, angle)
            time.sleep(0.5)
        for angle in range(240, -1, -10):  # Move down
            set_servo_angle(servo_id, angle)
            time.sleep(0.5)
except KeyboardInterrupt:
    print("Stopping servo control.")
finally:
    ser.close()
