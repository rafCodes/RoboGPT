# Raphael Fortuna (raf269) 
# Rabail Makhdoom (rm857) 
# Final Project Report
# Lab 403, Lab Section:  4:30pm-7:30pm on Thursdays 

import pygame     # Import pygame graphics library
from pygame.locals import *   # for event MOUSE variables
import os    # for OS calls
import time
from importlib.machinery import SourceFileLoader

prePath = "/home/pi/"

directPaths = prePath + "RoboGPT/src/"

# import library
pin_config = SourceFileLoader("pin_config", directPaths + "pin_config.py").load_module()

# set os environment variables for pygame
os.putenv('SDL_VIDEODRIVER', 'fbcon')   # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb0')     
os.putenv('SDL_MOUSEDRV', 'TSLIB')     # Track mouse clicks on piTFT 
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
pygame.init()

# hide the mouse cursor
pygame.mouse.set_visible(False)

WHITE = 255, 255, 255
BLACK = 0,0,0

class display:

    def __init__(self):
        self.screen = pygame.display.set_mode((320, 240))
        self.my_font = pygame.font.Font(None, 35)
        self.fifo_path = pin_config.fifo_path

        # data in from the fifo
        self.dataIn = ""

        self.clearScreen()

    def clearScreen(self):
        """ Erase the Work space """
        self.screen.fill(BLACK)

    def showText(self, text: list):
        """ write text to the middle of the screen """

        print(text)

        self.clearScreen()

        yGap = 30

        centerX = 160
        centerY = 120

        font = self.my_font

        if len(text) > 8:
            font = pygame.font.Font(None, 25)
            yGap = 20
            text = text[:8] # cut off the text to avoid running off the screen

        centerY -= int(yGap * len(text) / 2)

        for i in range(len(text)):
            # draw the text on the screen
            text_surface = self.my_font.render(text[i], True, WHITE)    
            rect = text_surface.get_rect(center=(centerX, centerY))
            self.screen.blit(text_surface, rect)

            centerY += yGap

        pygame.display.flip()

    def drawResumeButton(self):
        """ Writes text that points to the resume button """

        self.clearScreen()

        # draw the text on the button
        text_surface = self.my_font.render("Resume   ->", True, WHITE)    
        rect = text_surface.get_rect(center=(240, 220))
        self.screen.blit(text_surface, rect)
        pygame.display.flip()

    def fifo_read(self):
        """ read data in from the fifo """
        dataOut = ""
        fifo_fd = os.open(self.fifo_path, os.O_RDONLY)
        while True:
            data = os.read(fifo_fd, 1024)
            if len(data) == 0:
                break
            dataOut = data.decode()
        os.close(fifo_fd)
        return dataOut
    

    def loopCycle(self):
        """ this is what will monitor the fifo and display the results """
        self.dataIn = ""

        while self.dataIn != "quit":
            
            # check for new data
            new_data = self.fifo_read()

            if new_data != self.dataIn:
                print("new data: " + new_data)

                if new_data != "quit":

                    processed = new_data.replace('\n', '')

                    # now check if is running a function or sending text
                    if processed == pin_config.resume_fifo:
                        self.drawResumeButton()
                    else:
                        # remove \n from text
                        textIn = processed.split(',')
                        self.showText(textIn)

                # without processing so that does not keep updating the screen with the same text
                self.dataIn = new_data
    
if __name__ == "__main__":
    d = display()
    d.loopCycle()