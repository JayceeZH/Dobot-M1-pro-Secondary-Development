import threading
from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove, MyType
from time import sleep
import numpy as np

PARAMS=0
def connect_robot():
    try:
        ip = "192.168.1.6"
        dashboard_p = 29999
        move_p = 30003
        feed_p = 30004
        print("Connecting...")
        dashboard = DobotApiDashboard(ip, dashboard_p)
        move = DobotApiMove(ip, move_p)
        feed = DobotApi(ip, feed_p)
        print(">.< Success Connection >!<")
        return dashboard, move, feed
    except Exception as e:
        print(":( Failed to connect:(")
        raise e

if __name__ == '__main__':
    dashboard, move, feed = connect_robot()
   
    """
    ************************************
    ************************************
        if PARAMS  compiling condition, check whether parameters are included in commands
            0  No parameters
            1   Parameters exist
            
        Including samples：
            EnableRobot
            DisableRobot
            DO
            AccJ
            SetArmOrientation
            RunScript
            PositiveSolution
            InverseSolution
            ModbusCreate
            GetHoldRegs
            DOGroup
            MovL
            MovLIO
            MoveJog
            Circle
    """
    
    """
    ************************************
    ************************************
     * Command：EnableRobot
     * Function：enable robot
    """
    if PARAMS:
      dashboard.EnableRobot()    #No parameters
    else:
       load=0.1
       centerX=0.1
       centerY=0.1
       centerZ=0.1
       dashboard.EnableRobot(load)    #One parameter
       
       dashboard.EnableRobot(load, centerX, centerY, centerZ)    #Four parameters
  
    """
    ************************************
    ************************************
     * Command：DisableRobotexit
     * Function: disable robot
    """
    dashboard.DisableRobot()    #No parameters
     
     
    """
    ************************************
    ************************************
     * Command： DO
     * Function：set up digital output port status (queue command)
    """
    index=1
    status=1
    dashboard.DO(index,status)  
     
     
    """
     *******************************
     *******************************
     * Command： AccJ
     * Function：set up joint acceleration ratio, only available for commands MovJ, MovJIO, MovJR, JointMovJ
    """
    index=1
    dashboard.AccJ(index)  
     
     
    """
     ******************************
     ******************************
     * Command： SetArmOrientation
     * Function：set arm orientation
    """
    if PARAMS:
        LorR=1
        dashboard.SetArmOrientation(LorR)    #one parameter
    else:
        LorR=1
        UorD=1
        ForN=1
        Config=1
        dashboard.SetArmOrientation(LorR, UorD, ForN, Config)    #four parameters
    
    
    """
    ************************************
    ************************************
     * Command： RunScript
     * Function：run .lua scripts
    """
    name="luaname"
    dashboard.RunScript(name)  
     
    """
    ************************************
    ************************************
     * Command： PositiveSolution
     * Function：forward kinematics (joint -> Cartesian)
    """
    J1=0.1
    J2=0.1
    J3=0.1
    J4=0.1
    User=1
    Tool=1
    dashboard.PositiveSolution(J1, J2, J3, J4,User, Tool)    # one parameter

     
    """
    ************************************
    ************************************
     * Command： InverseSolution
     * Function：Inverse kinematics (Cartesian -> joint)
    """  
    if PARAMS:
        J1=0.1
        J2=0.1
        J3=0.1
        J4=0.1
        User=1
        Tool=1
        dashboard.InverseSolution(J1, J2, J3, J4,User, Tool)    # one parameter
    else:
        J1=0.1
        J2=0.1
        J3=0.1
        J4=0.1
        User=1
        Tool=1
        isJointNear=1
        JointNear="JointNear"
        dashboard.InverseSolution(J1, J2, J3, J4,User, Tool,isJointNear, JointNear)  
        
    """
    ************************************
    ************************************
     * Command： ModbusCreate
     * Function：create modbus
    """
    if PARAMS:
        ip="192.168.1.6"
        port=29999
        slave_id=1
        dashboard.ModbusCreate(ip, port, slave_id)
    else:
        ip="192.168.1.6"
        port=29999
        slave_id=1
        isRTU=1
        dashboard.ModbusCreate(ip, port, slave_id, isRTU)
     
     
    """
    ************************************
    ************************************
     * Command： GetHoldRegs
     * Function：read and hold registers
       """
    if PARAMS:
        index=1
        addr=1
        count=1
        dashboard.GetHoldRegs(index, addr, count)
    else:
        index=1
        addr=1
        count=1
        valType="valType"
        dashboard.GetHoldRegs(index, addr, count, valType)  
     
    """
    ************************************
    ************************************
     * Command： DOGroup
     * Function：set up and output group port status (maximum 64 parameters)
    """
    if PARAMS:
        index=1
        value=1
        dashboard.DOGroup(index, value)    # 2 parameters
    else:
        index=1
        value=1
        index2=1
        value2=1
        index32=1
        value32=1
        dashboard.DOGroup(index, value, index2, value2, index32, value32)    # 64 parameters (ignore the rest)
     
     
    """
    ************************************
    ************************************
     * Command： MovL
     * Function: point-to-point movement, Cartesian coordinates
    """
    if PARAMS:
        x=1.0
        y=1.0
        z=1.0
        r=1.0
        move.MovL(x, y, z, r)    #no parameters to be selected
    else:
        x=1.0
        y=1.0
        z=1.0
        r=1.0
        userparam="User=1"
        toolparam="Tool=1"
        speedlparam="SpeedL=1"
        acclparam="AccL=1"
        cpparam="CP=1" 
        move.MovL(x, y, z, r,userparam)    #input user, inputs order can be adjusted
        move.MovL(x, y, z, r,userparam, toolparam)    #set up user tool
        move.MovL(x, y, z, r,userparam, toolparam, speedlparam,)    #set up user  tool  speedl 
        move.MovL(x, y, z, r,userparam, toolparam, speedlparam, acclparam)    # set up user  user  tool  speedl accl
        move.MovL(x, y, z, r,userparam, toolparam, speedlparam, acclparam, cpparam)    #set up user  tool  speedl accl cp
     
     
    """
    ************************************
    ************************************
    * Command： Arc
    * Function：Move from the current position to the target in the Cartesian coordinate system by circular interpolation.
      This command should be combined with other motion commands to determine the starting point of the arc.
    """
    if PARAMS:
        x=1.0
        y=1.0
        z=1.0
        r=1.0
        x2=1.0
        y2=1.0
        z2=1.0
        r2=1.0
        move.Arc(x, y, z, r,x2, y2, z2, r2)
    else:
        x=1.0
        y=1.0
        z=1.0
        r=1.0
        x2=1.0
        y2=1.0
        z2=1.0
        r2=1.0
        userparam="User=1"
        toolparam="Tool=1"
        speedlparam="SpeedL=1"
        acclparam="AccL=1"
        cpparam="CP=1" 
        move.Arc(x, y, z, r,x2, y2, z2, r2,cpparam,userparam,speedlparam, toolparam, speedlparam, acclparam)    # user tool order cannot be adjusted
 
 
    """
    ************************************
    ************************************
     * Command： MovLIO
     * Function：The state of the digital output port is set in parallel during linear trajectory movements, 
                 target point is the Cartesian coordinates.
    """
    if PARAMS:
        x=1.0
        y=1.0
        z=1.0
        r=1.0
        Mode=1
        Distance=1
        Index=1
        Status=1
        move.MovLIO(x, y, z, r, Mode, Distance, Index, Status)
    else:
        x=1.0
        y=1.0
        z=1.0
        r=1.0
        Mode=1
        Distance=1
        Index=1
        Status=1
        userparam="User=1"
        toolparam="Tool=1"
        speedlparam="SpeedL=1"
        acclparam="AccL=1"
        cpparam="CP=1" 
        move.MovLIO(x, y, z, r,Mode, Distance, Index, Status,cpparam,userparam,speedlparam, toolparam, speedlparam, acclparam)    # user tool order cannot be adjusted    
     
    """
    ************************************
    ************************************
     * Command： MoveJog
     * Function：point movements, distance not fixed
    """
    if PARAMS:
        axisID=""
        move.MoveJog(axisID)           
    else:
        axisID="j1+"
        CoordType="CoordType=0"
        userparam="User=0"
        toolparam="Tool=0"
        move.MoveJog(axisID, CoordType, userparam, toolparam)    

    ## send MoveJog() stop command to terminate robot movements
    move.MoveJog()
    
    
    """
    ************************************
    ************************************
     * Command： Circle
     * Function：circle movements, only available in Cartesian coordinates
    """   
    if PARAMS:
        x=1.0
        y=1.0
        z=1.0
        r=1.0
        count=1
        move.Circle(x, y, z, r,count)           
    else:
        x=1.0
        y=1.0
        z=1.0
        r=1.0
        count=1
        userparam="User=0"
        toolparam="Tool=0"
        speedlparam="SpeedL=R"
        acclparam="AccL=R"
        move.Circle(x, y, z, r,count, userparam, toolparam, speedlparam, acclparam)       