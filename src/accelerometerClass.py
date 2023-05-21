# Raphael Fortuna (raf269) 
# Rabail Makhdoom (rm857) 
# Final Project Report
# Lab 403, Lab Section:  4:30pm-7:30pm on Thursdays 

import time
import board
import busio
import math
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

class accelerometerClass:
    def __init__(self):

        # Create library object using our Bus I2C port
        self.i2c = board.I2C() # uses board.SCL and board.SDA
        self.sox = LSM6DSOX(self.i2c)

        self.acceleration = self.sox.acceleration
        self.gyro = self.sox.gyro

    def getAcceleration(self):
        """ get acceleration x, y, z """

        return self.acceleration
    
    def getGyro(self):
        """ get gyro x, y, z """

        return self.gyro

if __name__ == "__main__":

    # test code
    accel = accelerometerClass()

    while True:        
        print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (accel.acceleration))
        print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (accel.gyro))
        print("")
        time.sleep(0.5)
