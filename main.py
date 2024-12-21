import threading
from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove, MyType,alarmAlarmJsonFile
from time import sleep, time
import numpy as np
import re

# Global variables
current_actual = None
algorithm_queue = None
enableStatus_robot = None
robotErrorState = False
globalLockValue = threading.Lock()

def ConnectRobot():
    try:
        ip = "192.168.1.6"
        dashboardPort = 29999
        movePort = 30003
        feedPort = 30004
        print("Connecting...")
        dashboard = DobotApiDashboard(ip, dashboardPort)
        move = DobotApiMove(ip, movePort)
        feed = DobotApi(ip, feedPort)
        print(">.< Successful Connection >!<")
        return dashboard, move, feed
    except Exception as e:
        print(":( Failed to connect :(")
        raise e

def RunPoint(move: DobotApiMove, point: tuple):
    if len(point) != 4:
        raise ValueError(f"Point must have exactly 4 elements (x, y, z, r), but got: {point}")
    move.JointMovJ(point[0], point[1], point[2], point[3])


def GetFeed(feed: DobotApi):
    global current_actual
    global algorithm_queue
    global enableStatus_robot
    global robotErrorState
    hasRead = 0
    while True:
        data = bytes()
        while hasRead < 1440:
            temp = feed.socket_dobot.recv(1440 - hasRead)
            if len(temp) > 0:
                hasRead += len(temp)
                data += temp
        hasRead = 0
        feedInfo = np.frombuffer(data, dtype=MyType)
        if hex((feedInfo['test_value'][0])) == '0x123456789abcdef':
            globalLockValue.acquire()
            # Refresh Properties
            current_actual = feedInfo["tool_vector_actual"][0]
            algorithm_queue = feedInfo['isRunQueuedCmd'][0]
            enableStatus_robot=feedInfo['EnableStatus'][0]
            robotErrorState= feedInfo['ErrorStatus'][0]
            globalLockValue.release()
        sleep(0.001)

def WaitArrive(point_list):
    while True:
        is_arrive = True
        globalLockValue.acquire()
        if current_actual is not None:
            for index in range(4):
                if (abs(current_actual[index] - point_list[index]) > 1):
                    is_arrive = False
            if is_arrive :
                globalLockValue.release()
                return
        globalLockValue.release()  
        sleep(0.001)

def ClearRobotError(dashboard: DobotApiDashboard):
    global robotErrorState
    dataController,dataServo =alarmAlarmJsonFile()    # Input controller and servo alarm state
    while True:
      globalLockValue.acquire()
      if robotErrorState:
                numbers = re.findall(r'-?\d+', dashboard.GetErrorID())
                numbers= [int(num) for num in numbers]
                if (numbers[0] == 0):
                  if (len(numbers)>1):
                    for i in numbers[1:]:
                      alarmState=False
                      if i==-2:
                          print("Alarm: Collisions!",i)
                          alarmState=True
                      if alarmState:
                          continue                
                      for item in dataController:
                        if  i==item["id"]:
                            print("Controller errorID",i,item["en"]["description"])
                            alarmState=True
                            break 
                      if alarmState:
                          continue
                      for item in dataServo:
                        if  i==item["id"]:
                            print("Servo errorID",i,item["en"]["description"])
                            break  
                       
                    choose = input("Input 1 will clear error logs and device keeps running: ")     
                    if  int(choose)==1:
                        dashboard.ClearError()
                        sleep(0.01)
                        dashboard.Continue()

      else:  
         if int(enableStatus_robot[0])==1 and int(algorithm_queue[0])==0:
            dashboard.Continue()
      globalLockValue.release()
      sleep(5)
      
# Function to process each point
def process_point(point):
    # Add processing logic for each point here
    print(f"Processing point: {point}")
       
if __name__ == '__main__':
    dashboard, move, feed = ConnectRobot()
    print("Start enabling...")
    dashboard.EnableRobot()
    print("Enabled:)")
    feed_thread = threading.Thread(target=GetFeed, args=(feed,))
    feed_thread.setDaemon(True)
    feed_thread.start()
    feed_thread1 = threading.Thread(target=ClearRobotError, args=(dashboard,))
    feed_thread1.setDaemon(True)
    feed_thread1.start()
    print("Loop execution...")
    # point_a = [20, 280, -60, 200]
    # point_b = [160, 260, -30, 170]
    point_c = [-11.82, -25.38, 201.26, 123.69]
    
while True:
    with open('joint_coordinates.txt', 'r') as file:
        for line_num, line in enumerate(file, 1):
            try:
                # Parse line into coordinates, assuming they are separated by commas
                point = [float(value.strip()) for value in line.split(',')]
                
                # Ensure there are exactly 4 values for joint coordinates (adjust this as needed)
                if len(point) != 4:
                    print(f"Error in line {line_num}: Expected 4 joint coordinates but found {len(point)}")
                    continue
                
                # Process the point
                process_point(point)
                
                # Run the move and wait for the robot to arrive at the point
                ip = "192.168.1.6"
                movePort = 30003
                move = DobotApiMove(ip, movePort)
                try:
                    RunPoint(move, point)
                    sleep(1)
                except Exception as e:
                    print(f"Error in RunPoint: {e}")
                
                # try:
                #     WaitArrive(point)
                # except Exception as e:
                #     print(f"Error in WaitArrive: {e}")

            except ValueError as e:
                print(f"Error processing line {line_num}: {e}")

        # If no points were successfully processed, wait and retry
        if not point:
            print("No valid points found in the file. Waiting before retry...")
            # Optionally add a delay here to avoid busy-looping
            sleep(1)  # Adjust the sleep time if needed


# #For single point test only
# while True:
#     ip = "192.168.1.6"
#     movePort = 30003
#     move = DobotApiMove(ip, movePort)
#     point = [-11.82, -25.38, 201.26, 123.69]
#     try:
#         RunPoint(move, point)
#     except Exception as e:
#         print(f"Error in RunPoint: {e}")
    
#     try:
#         WaitArrive(point)
#     except Exception as e:
#         print(f"Error in WaitArrive: {e}")

    # # Optionally add a delay before reopening the file and processing the next set of points
    # time.sleep(1)  # Adjust the sleep time if needed