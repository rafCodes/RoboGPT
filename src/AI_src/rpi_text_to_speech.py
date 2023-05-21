# Raphael Fortuna (raf269) 
# Rabail Makhdoom (rm857) 
# Final Project Report
# Lab 403, Lab Section:  4:30pm-7:30pm on Thursdays 

import requests
import os
import time
import vlc
from mutagen.mp3 import MP3

class text_to_speech:

    def __init__(self, debug = False, voice_on = True, voice_gender = 'Male', voice = "en-AU-KenNeural"):
        self.url = "https://"+ os.environ.get('ROVER_SPEECH_REGION') + ".tts.speech.microsoft.com/cognitiveservices/v1"
        self.headers = {
            'Ocp-Apim-Subscription-Key': os.environ.get('ROVER_SPEECH_KEY'),
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'audio-16khz-128kbitrate-mono-mp3',
            'User-Agent': 'python-requests'
        }

        self.dataFront = "<speak version='1.0' xml:lang='en-US'>"
        self.dataFront += "<voice xml:lang='en-US' xml:gender='"+ voice_gender
        self.dataFront += "' name='"+ voice +"'>"

        self.dataBack = "</voice></speak>"

        # to turn off the voice if needed
        self.voice_on = voice_on

        self.debug = debug

        self.fileLocation = "/home/pi/output.mp3"

    def speak_text(self, text):
        """ speak the text """

        if self.voice_on:

            data = self.dataFront + str(text) + self.dataBack

            response = requests.post(self.url, headers=self.headers, data=data)

            if (response.status_code != 200):
                print("Got error code {} when using text to speech".format(response.status_code))
                print(response.text)
                quit()

            with open(self.fileLocation, "wb") as f:
                f.write(response.content)
        try:
            self.say_text_vlc()
        except:
            print('vlc threw an error')

    def say_text_vlc(self):
        """ speak the text after it is saved with vlc 
        
        note: this is a blocking function
        pygame did not work

        VLC has a memory leak after a long while of usage (10-15 min), fix is to restart the python instance of manager.py
        
        """
        p = vlc.MediaPlayer(self.fileLocation)

        # get length of file
        length = MP3(self.fileLocation).info.length

        p.play()

        # wait for the file to finish
        time.sleep(length)

if __name__ == "__main__":
    tts = text_to_speech(debug=True)
    tts.speak_text("Hello World, this is a long sentence")