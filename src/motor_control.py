# Raphael Fortuna (raf269) 
# Rabail Makhdoom (rm857) 
# Final Project Report
# Lab 403, Lab Section:  4:30pm-7:30pm on Thursdays 

import time
import board
import pigpio # run sudo pigpiod to start daemon
import subprocess #to start pigpiod
from importlib.machinery import SourceFileLoader

prePath = "/home/pi/"

directPaths = prePath + "RoboGPT/src/"
AICorePaths = prePath + "RoboGPT/src/AI_src/"

# import libraries
pin_config = SourceFileLoader("pin_config", directPaths + "pin_config.py").load_module()
utils = SourceFileLoader("utils", AICorePaths + "utils.py").load_module()

class motorControl:
       
        def __init__(self):
                self.GPIO_Scale = 1000000 # 1,000,000 microseconds = 1 second
                self.freq = 50 # 50Hz

                self.left = pin_config.left_pin
                self.right = pin_config.right_pin

                # text color
                self.color = "yellow" 

                # try to kill daemon if running since can cause drift if run for long time
                try:
                        subprocess.check_output('sudo killall pigpiod', shell=True)
                except:
                        print("Daemon was not intially running")

                time.sleep(1)

                # start up pigpio daemon, 2x since can fail first time
                subprocess.check_output('sudo pigpiod', shell=True)

                time.sleep(1)

                subprocess.check_output('sudo pigpiod', shell=True)
                
                self.pi_hw = pigpio.pi() #connect to pi gpio daemon
                
                self.Calibrate()
                self.stop()


        def getDutyCycle(self, pulse_d):
                """ get the GPIO duty cyle from the time of the pulse"""

                pulse = 20 + pulse_d
                percentPulse = pulse_d / pulse
                p_out = percentPulse * self.GPIO_Scale

                return int(p_out)
        
        def Calibrate(self):
                """ Calibrate the motors"""
                utils.color_printer(self.color, "Calibrating motors")
                print("Calibrate")
                self.pi_hw.hardware_PWM(self.right, self.freq, self.getDutyCycle(1.5))
                self.pi_hw.hardware_PWM(self.left, self.freq, self.getDutyCycle(1.5))
                time.sleep(3.0)
                

        def turnLeft(self):
                """ Turn left """
                # Moving Left 
                utils.color_printer(self.color, "Moving left")
                self.pi_hw.hardware_PWM(self.right, self.freq, self.getDutyCycle(1.3))
                self.pi_hw.hardware_PWM(self.left, self.freq, self.getDutyCycle(1.35))


        def turnRight(self):
                """ Turn right """
                # Moving Right
                utils.color_printer(self.color, "Moving right")
                self.pi_hw.hardware_PWM(self.right, self.freq, self.getDutyCycle(1.7))
                self.pi_hw.hardware_PWM(self.left, self.freq, self.getDutyCycle(1.7))


        def moveStraight(self):
                """ Move Straight"""
                utils.color_printer(self.color, "Moving straight")
                self.pi_hw.hardware_PWM(self.left, self.freq, self.getDutyCycle(1.7))
                self.pi_hw.hardware_PWM(self.right, self.freq, self.getDutyCycle(1.4))
                
        def moveBack(self):
                """ Move Back"""
                utils.color_printer(self.color, "Moving back")
                self.pi_hw.hardware_PWM(self.left, self.freq, self.getDutyCycle(1.4))
                self.pi_hw.hardware_PWM(self.right, self.freq, self.getDutyCycle(1.7))

        def stop(self):
                """ Stop the motors """
                utils.color_printer(self.color, "Stopping")
                self.pi_hw.hardware_PWM(self.left, self.freq,  0)
                self.pi_hw.hardware_PWM(self.right, self.freq, 0)

if __name__ == "__main__":
        motor = motorControl()
        motor.moveBack()
        time.sleep(1.3)
        motor.turnRight()
        time.sleep(1.3)
        motor.stop()
        time.sleep(1.0)
 