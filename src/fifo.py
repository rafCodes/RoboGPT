# Raphael Fortuna (raf269) 
# Rabail Makhdoom (rm857) 
# Final Project Report
# Lab 403, Lab Section:  4:30pm-7:30pm on Thursdays 

import subprocess
import os

class displayFifo():
    def __init__(self, fifoPath):
        self.fifoPath = fifoPath

    def sendCommand(self, text):
        """ send a command to the fifo for the display to read """

        my_cmd = 'echo "' + text + '" > ' + self.fifoPath

        # use subprocess call to send 'my_cmd' to the linux shell for execution
        subprocess.check_output(my_cmd, shell=True)