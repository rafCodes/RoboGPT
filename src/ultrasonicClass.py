# Raphael Fortuna (raf269) 
# Rabail Makhdoom (rm857) 
# Final Project Report
# Lab 403, Lab Section:  4:30pm-7:30pm on Thursdays 

import RPi.GPIO as GPIO
import time
import numpy as np
from importlib.machinery import SourceFileLoader

prePath = "/home/pi/"

pinPath = prePath + "RoboGPT/src/pin_config.py"

# imports the module from the given path
pin_config = SourceFileLoader("pin_config", pinPath).load_module()

import adafruit_hcsr04
import board

class _controlUltrasonicWAda:
    """ class to control a ultrasonic sensor using the adafruit library """

    def __init__(self, TRIGGER, ECHO):

        # trigger and echo are int, get correct GPIO from board
        self.TRIGGER = getattr(board, "D" + str(TRIGGER))
        self.ECHO = getattr(board, "D" + str(ECHO))
        self.distance = 0
        self.min = 1

        # how many samples needed before returning a value
        self.sampleCount = 5

        self.sensor = adafruit_hcsr04.HCSR04(trigger_pin=self.TRIGGER, echo_pin=self.ECHO)
        print("Sensor initialized")

        self.attempts = 20*self.sampleCount # number of times to try to get a reading

    def getDistance(self):
        """ return the distance in cm """

        gotValue = False
        distance = 0
        attempts = 0

        samples = []

        while len(samples) < self.sampleCount:
            try:
                distance = self.sensor.distance
                if (distance > self.min):
                    gotValue = True
                    samples.append(distance)
            except RuntimeError:
                attempts += 1
                if (attempts > self.attempts):
                    print("Could not get distance")
                    print("Sending old distance")
                    return self.distance
                pass

        # get median of the samples to reduce noise
        samples = np.array(samples)
        distance = np.median(samples)

        self.distance = distance

        return distance
    
class frontUltrasonic(_controlUltrasonicWAda):
    """ class for the front ultrasonic sensor """

    def __init__(self):
        super().__init__(pin_config.front_trigger, pin_config.front_echo)

class backUltrasonic(_controlUltrasonicWAda):
    """ class for the back ultrasonic sensor """

    def __init__(self):
        super().__init__(pin_config.back_trigger, pin_config.back_echo)


if __name__ == "__main__":
    # test code
    front_sensor = frontUltrasonic()
    back_sensor = backUltrasonic()

    while True:
        # print the time it took for each reading
        start_time = time.time()
        front_distance = front_sensor.getDistance()
        end_time = time.time()
        print("front: ", front_distance, " time: ", end_time - start_time)

        start_time = time.time()
        back_distance = back_sensor.getDistance()
        end_time = time.time()
        print("back: ", back_distance, " time: ", end_time - start_time)

        time.sleep(1)
