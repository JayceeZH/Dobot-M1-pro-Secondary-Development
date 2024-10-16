import os
import sys
from Arduino.Arduino import Arduino
from time import sleep

cwd = os.getcwd()
(setpath, Examples) = os.path.split(cwd)
sys.path.append(setpath)

class TEST_FIRMWARE:
    def __init__(self, baudrate):
        self.baudrate = baudrate
        self.setup()
        self.run()
        self.exit()
    def setup(self):
        self.obj_arduino = Arduino()
        self.port = self.obj_arduino.locateport()
        self.obj_arduino.open_serial(1, self.port, self.baudrate)
    def run(self):
        self.obj_arduino.checkfirmware()
    def exit(self):
        self.obj_arduino.close_serial()

def main():
    obj_servo = TEST_FIRMWARE(115200)
if __name__ == '__main__':
    main()