# Raphael Fortuna (raf269) 
# Rabail Makhdoom (rm857) 
# Final Project Report
# Lab 403, Lab Section:  4:30pm-7:30pm on Thursdays 

import os
import speech_recognition as sr

class speech_to_text:
    """ class to convert speech to text """

    def __init__(self, fifo_function = None, debug = False):
        self.speech_engine = sr.Recognizer()
        self.current_audio = None
        self.collected_text = ""
        self.debug = debug

        self.fifo_function = fifo_function
        self.mic = sr.Microphone() # default microphone

    def get_speech_text(self):
        """ collect speech from the microphone and return the text 
        
        True/False used to make sure actually got text, then can collect it using get_collected_text()
        
        """

        with self.mic as source:
            if (self.debug):
                print("Speak into your microphone.")
            print("What should I do")

            # display message on the robot TFT screen
            if self.fifo_function is not None:
                self.fifo_function("What should I do?")
            self.speech_engine.adjust_for_ambient_noise(source) # adjust audio for ambient noise
            self.current_audio = self.speech_engine.listen(source, timeout = 8, phrase_time_limit = 10)

        try:
            collected_data = self.speech_engine.recognize_azure(self.current_audio, 
                                                                     key = os.environ.get('ROVER_SPEECH_KEY'), 
                                                                     location = os.environ.get('ROVER_SPEECH_REGION'))
            self.collected_text = collected_data[0]

            # display message on the robot TFT screen
            if self.fifo_function is not None:
                self.fifo_function("Done collecting Speech")
            return True
        
        except sr.UnknownValueError as e:
            print("Could not understand audio; {0}".format(e))
            return False
        
        except sr.RequestError as e:
            print("Could not request results from Azure Speech Recognition service; {0}".format(e))
            return False
        
        except sr.WaitTimeoutError as e:
            print("Waiting for text... Took too long, try again")
            return False

    def get_collected_text(self):
        """ return the collected text """
        return self.collected_text
    
if __name__ == "__main__":
    speech_instance = speech_to_text(debug = True)
    if speech_instance.get_speech_text():
        print(speech_instance.get_collected_text())