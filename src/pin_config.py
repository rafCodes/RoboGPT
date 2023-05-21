# Raphael Fortuna (raf269) 
# Rabail Makhdoom (rm857) 
# Final Project Report
# Lab 403, Lab Section:  4:30pm-7:30pm on Thursdays 

import time

prePath = "/home/pi/"

# motor pins
left_pin = 13
right_pin = 12

# ultrasonic pins
front_trigger = 16
front_echo = 21
back_trigger = 20
back_echo = 23

# Path for the fifo

fifo_path = prePath + 'RoboGPT/src/display_fifo'

# accelerometer uses i2c and the adafruit library (using SDA and SCL)

# hardware button pins
text_swap_button = 22
resume = 27

# specific string for to send and check for
resume_fifo = "resume"


class actionUnit:
    """ used to keep track of how long a action should be performed and if it is done"""

    def __init__(self, time_period, action_name, action_value):
        self.time_period = time_period
        self.action_name = action_name
        self.action_value = action_value

        self.pausedTime = 0

        self.start_time = time.time()

    def isDone(self):
        """ return true if the action is done """

        if time.time() - self.start_time >= self.time_period:
            return True

        return False

    def toString(self):
        """ action unit to string"""
        return self.action_name + ": " + self.action_value
