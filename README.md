# ECE 5725 Final Project: RoboGPT, an AI Powered Robot

## Team Members
- Raphael Fortuna
- Rabail Makhdoom

## Summary
We chose to build a robot that can be controlled by ChatGPT to perform various tasks like driving around it different shapes or even playing a game with the. The robot is equipped a USB microphone, two ultrasonic sensors, and an accelerometer and gyroscope.

This robot takes in speech using Azure Speech Services and converts it to text. This text is then sent to ChatGPT, which generates a response. The response is then sent back to the robot, which performs the task and responds back to the user using Azure Speech Services text-to-speech using a speaker. The sensor data is also sent to ChatGPT so that it can be aware of its surroundings.

### Note:
If you are interested in just running the robot core that converts high level requests to low level robot commands without a Raspberry Pi, you can skip the CircuitPython installation step and only use the files in AI_src as they are hardware independent. 

## Installation instructions

Please see our website, found [here (to be added soon)]() for looking at the full inner working of the robot, testing process, and the circuit diagrams for the hardware.

This repository uses importlib machinery's SourceFileLoader to avoid having issues with where the code is being run and is set to run in **home/pi/**.

If it is in a different location, modify the prePath variable at the top of each file to match your location in the following files:

- manager.py  
- motor_control.py  
- pin_config.py
- ultrasonicClass.py
- robot_core.py
- chat_conversation.py
- display.py

### Software

You will first need to install CircuitPython from Adafruit for the ultrasonic sensors and accelerometer and gyroscope.

At the time of writing and for our Raspberry Pi 4B running a 32-Bit OS, we used:

```
sudo pip3 install --upgrade adafruit-python-shell

wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py

sudo python3 raspi-blinka.py

pip3 install adafruit-circuitpython-bme280
```

More information can be found on the Adafruit website at the following links:
- [Starting with CircuitPython](https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries)
- [Raspberry Pi 4B CircuitPython installation instructions](https://circuitpython.org/blinka/raspberry_pi_4b/)
- [I2C address, enabling I2C, and pins](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/i2c-sensors-and-devices)
- [I2C Protocol overview](https://learn.adafruit.com/i2c-addresses)
- [I2C list of addresses](https://learn.adafruit.com/i2c-addresses/the-list)

With CircuitPython installed, you can install all the required packages using the requirements.txt file by running:
    
```
pip install -r requirements.txt
```

You must also set environment variables for
- ROVER_SPEECH_KEY with your Azure Speech Services key
- ROVER_SPEECH_REGION with your Azure Speech Services region
- ROVER_OPENAI_KEY with your OpenAI API key for using ChatGPT

You will also need to install a piTFT and the drivers that it requires for your Raspberry Pi. If you do not have a piTFT display, then do not run display.py. It was intentionally decoupled from manager.py to support this.

## Running the code

Once you have installed all your libraries and built the circuits, you can run manager.py to start the robot and display.py to start the display on the piTFT

## Known Issues
The python-vlc package was the only audio library that consistently worked with our software and hardware setup and can be changed in rpi_text_to_speech.py if you have issues with it. 

## Software Extras

During our development process, we switched from using the azure-cognitiveservices-speech package to using SpeechRecognition, REST API for text-to-speech, and VLC for audio. This was due to our Raspberry Pi using a 32-Bit OS and the azure-cognitiveservices-speech package requiring a 64-Bit OS and the Micorosoft Visual C++ Redistributiable for Visual Studio, with more information that can be found [here](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-text-to-speech?pivots=programming-language-python&tabs=windows%2Cterminal).

You can optionally install it to use the speech_to_text.py and text_to_speech.py that were replaced by rpi_speech_to_text.py and rpi_text_to_speech.py.

This package can be installed by running:
    
```
pip install azure-cognitiveservices-speech
```



