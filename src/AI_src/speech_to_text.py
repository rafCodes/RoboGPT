# Raphael Fortuna (raf269) 
# Rabail Makhdoom (rm857) 
# Final Project Report
# Lab 403, Lab Section:  4:30pm-7:30pm on Thursdays 

import os
import azure.cognitiveservices.speech as speechsdk

class speech_to_text:
    
    def __init__(self, debug = False):
        self.speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('ROVER_SPEECH_KEY'), region=os.environ.get('ROVER_SPEECH_REGION'))
        self.speech_config.speech_recognition_language="en-US"
        self.audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        # side note:
        # param device_name: Specifies the id of the audio device to use.
        # Please refer to `this page <https://aka.ms/csspeech/microphone-selection>`
        # on how to retrieve platform-specific microphone names. This functionality was added in version 1.3.0.

        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_config)

        self.debug = debug

        self.collected_text = ""

    def get_speech_text(self):
        """ collect speech from the microphone and return true if got text """

        if self.debug:
            print("Speak into your microphone.")
        
        speech_recognition_result = self.speech_recognizer.recognize_once_async().get()
            
        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            if self.debug:
                print("Recognized: {}".format(speech_recognition_result.text))
            self.collected_text = speech_recognition_result.text
            return True
            
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            if self.debug:
                print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
                self.collected_text = ""
            return False

        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details

            if self.debug:
                print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                self.collected_text = ""

                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")
            return False

    def get_collected_text(self):
        """ return the collected text from the microphone """

        return self.collected_text
    

if __name__ == "__main__":
    speech_instance = speech_to_text(debug = True)
    if speech_instance.get_speech_text():
        print(speech_instance.get_collected_text())