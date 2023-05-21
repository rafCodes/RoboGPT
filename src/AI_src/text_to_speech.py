# Raphael Fortuna (raf269) 
# Rabail Makhdoom (rm857) 
# Final Project Report
# Lab 403, Lab Section:  4:30pm-7:30pm on Thursdays 

import os
import azure.cognitiveservices.speech as speechsdk

class text_to_speech:
    def __init__(self, debug = False, voice_on = True, voice = "en-AU-KenNeural"):
        self.speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('ROVER_SPEECH_KEY'), region=os.environ.get('ROVER_SPEECH_REGION'))
        self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

        # to disable the voice if needed
        self.voice_on = voice_on

        # The language of the voice that speaks.
        self.speech_config.speech_synthesis_voice_name = voice

        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
        self.debug = debug

    def speak_text(self, text):
        """ speak the text """

        # only speak if turned on, easier to debug this way
        if self.voice_on:
            if self.debug:
                print("Speaking: {}".format(text))
            
            speech_synthesis_result = self.speech_synthesizer.speak_text_async(text).get()

            if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                if self.debug:
                    print("Speech synthesized for text [{}]".format(text))
                return True
            elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = speech_synthesis_result.cancellation_details
                if self.debug:
                    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
                    if cancellation_details.reason == speechsdk.CancellationReason.Error:
                        print("Error details: {}".format(cancellation_details.error_details))
                        print("Did you set the speech resource key and region values?")
                return False

if __name__ == "__main__":
    text_instance = text_to_speech(debug = True)
    text_instance.speak_text("Hello World")