# Dobot-M1-pro-Secondary-Development
## Getting Ready
1. After connection between M1-pro and your PC through LAN cable, PC IP address is required to be in the same network segment with M1-pro controller. Default IP address of controller LAN1 is 192.168.1.6, which is currently connected.
2. Steps for PC network segment modification:
<br> - Search "View Network Connections"
<br> - Right-click "Properties" on currently-connected network
<br> - Double-click "Internet Protocol Version 4(TCP/IPv4)"
<br> - Select "Use the following IP address", change PC IP address to 192.168.1.6 and subnet mask to 255.255.255.0
3. For DobotStudio Pro control: after start, click "Start" for PC-M1pro connection.
4. For Python code control: clone repository into any folder you prefer, open main.py for secondary development tool execution.
5. More infomation about M1-pro hardware and DobotStudio Pro introduction please refer:
<br> [M1-pro hardware guide](./Dobot M1 Pro Hardware User Guide.pdf) 
<br> [DobotStudio Pro guide](./DobotStudio Pro User Guide MG400&M1 Pro V2.7.pdf)
## Tool Execution
1. Open "main.py", check port IP address is correct then execute it.
2. For modifying input target points, run `generate_XYZ.py`, output will be stored in file `cartesian_coordinates.txt`. Input coordinate data file is currently required in joint coordinates, `Q-learning.py` is working for converting Cartesian into joint coordinates. `joint_coordinates.txt` file stores all converted target coordinate data.


## Script Introduction
- `main.py`: works for tool execution, port IP definition. If you prefer other movement control functions, it can be modified in this script. Full control commands please refer `dobot_api.py`.
- `dobot_api.py`: stores full robot arm control command functions, system monitoring and communication information.
- `generate_XYZ.py`: creates 100 random Cartesian coordinates in defined range.
- `Inverse_Kinematics.py`: converts Cartesian coordinates to joint expression.
- `Q-learning.py`: executes inverse kinematics function, applies Q-learning techniques for ensuring output coordinates are valid (all involved in M1-pro working space).
###### Scripts below are not involved in the tool execution, just for tests:
- `ui.py` & `mainUI.py`: UI tool for secondary control.
- `PythonExample.py`: sample scripts for application provided by Dobot company.
- `random_joint.py`: generates random joint positions.
- `check_FW.py`: works for Arduino component firmware check.

## Debugging
#### Connection unsuccessful/device not responding: 
- Make sure M1-pro is enabled before uploading any movement commands.
- Check wire connection, port number and IP address. If necessary, try to disable WIFI connection and use LAN cable connection only. If issue remains, try rebooting devices and remodifying IP address.
#### Successful connection but M1-pro not moving: 
- If `WaitArrive()` function is enabled, try ignoring this function and reupload scripts to the device.
- Double check input target coordinates are valid.
#### For other issues not recorded in this document, please keep it updated.