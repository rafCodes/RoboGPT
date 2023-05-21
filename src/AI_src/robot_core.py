# Raphael Fortuna (raf269) 
# Rabail Makhdoom (rm857) 
# Final Project Report
# Lab 403, Lab Section:  4:30pm-7:30pm on Thursdays 

from importlib.machinery import SourceFileLoader

prePath = "/home/pi/"

# so that can be run from any directory
frontPath = prePath + "RoboGPT/src/AI_src/"

# try except to use the pi version of the code if running on the pi, removes having to change the code
try:
    import speech_to_text
except:
    # need the pi version
    speech_to_text = SourceFileLoader("speech_to_text", frontPath + "rpi_speech_to_text.py").load_module()

try:
    import text_to_speech
except:
    # need the pi version
    text_to_speech = SourceFileLoader("text_to_speech", frontPath + "rpi_text_to_speech.py").load_module()

try:
    import chat_conversation as openai_chat
    import utils
    from ai_config import robot_prompt, robot_max_tokens, robot_iteration_count

except:
    openai_chat = SourceFileLoader("openai_chat", frontPath + "chat_conversation.py").load_module()
    utils = SourceFileLoader("utils", frontPath + "utils.py").load_module()
    ai_config = SourceFileLoader("ai_config", frontPath + "ai_config.py").load_module()
    from ai_config import robot_prompt, robot_max_tokens, robot_iteration_count

class robot_core:

    def __init__(self, prompt = robot_prompt, 
                 max_tokens = robot_max_tokens, 
                 iteration_count = robot_iteration_count, 
                 voice_on = True, 
                 debug = False):
        
        # information used for the core's openai_chat instance
        self.prompt = prompt
        self.max_tokens = max_tokens

        # if the voice is on, false means that the robot will not speak
        self.voice_on = voice_on
        self.debug = debug

        self.chat_instance = openai_chat.openai_chat(system_prompt = self.prompt, debug = self.debug, max_tokens=self.max_tokens)
        self.text_instance = text_to_speech.text_to_speech(debug = self.debug, voice_on = self.voice_on)

        self.iteration_count = iteration_count

    def reboot_core(self):
        """ reboot the core if it ran out of memory """

        self.chat_instance = openai_chat.openai_chat(system_prompt = self.prompt, debug = self.debug, max_tokens=self.max_tokens)
        self.text_instance = text_to_speech.text_to_speech(debug = self.debug, voice_on = self.voice_on)

    def intialize_core(self):
        """" initalize the robot core 
        
        return: the assistant's response
        
        """
        self.chat_instance.init_chat()
        assistant_response = self.chat_instance.voice_chat("Please introduce yourself")
        self.text_instance.speak_text(assistant_response)

        return assistant_response
    
    def update_current_sensor_data(self, sensor_data, speak = False):
        """ update the current sensor data in the prompt """

        # uses system prompt to update the current sensor data
        output = self.chat_instance.voice_chat(sensor_data, extra = True, system = True)

        if output:
            # process the ### command ### out of the response for speaking and using it to control the robot
                            
            processedResponse, commandSequence = utils.process_commands(output)

            if commandSequence != []:
                utils.color_printer("red", str(commandSequence))

            if speak:
                self.text_instance.speak_text(processedResponse)
        
    def run_one_cycle(self, text_in):
        """ run one cycle of the core
        
        text_in: text to send to the assistant
        return: the assistant's response, commands to run
        
        """
        assistant_response = ""
        commandSequence = []

        # don't do anything if the user didn't say anything
        if text_in != "":
            assistant_response = self.chat_instance.voice_chat(text_in)

            if assistant_response:
                # process the ### command ### out of the response for speaking and using it to control the robot
                                
                processedResponse, commandSequence = utils.process_commands(assistant_response)

                if commandSequence != []:
                    utils.color_printer("red", str(commandSequence))

                if self.voice_on:
                    self.text_instance.speak_text(processedResponse)
        else:
            print("No text collected")

        return assistant_response, commandSequence

class full_cycle_demo(robot_core):

    # extends the class of robot core to make it easy to demo
    def __init__(self, prompt = robot_prompt, 
                 max_tokens = robot_max_tokens, 
                 iteration_count = robot_iteration_count, 
                 voice_on = True, 
                 debug = False,
                 generate_sensor_data = None):
        
        super().__init__(prompt, max_tokens, iteration_count, voice_on, debug)

        self.data_generator = None

        if generate_sensor_data != None:
            # add the synthetic data generator to the class
            self.data_generator = generate_sensor_data(debug = debug)
        
        # so can talk to the robot
        self.speech_instance = speech_to_text.speech_to_text(debug = debug)


    def _add_some_data(self):
        """ add some data to the conversation """

        sensor_data = ""

        if self.data_generator != None:
            sensor_data = self.data_generator.generate_data()

        return sensor_data

    def _run_one_demo_cycle(self, text_in):
        """ run one cycle of the demo 
        
        text_in: text to send to the assistant
        return: the assistant's response
        
        """

        sensor_data = self._add_some_data()

        assistant_response = ""
        
        # don't do anything if the user didn't say anything
        if text_in != "":
            total_text = text_in + '\n' + sensor_data
            self.chat_instance.voice_chat(sensor_data, extra = True, system = True)
            assistant_response = self.chat_instance.voice_chat(total_text)

            if assistant_response:
                # process the ### command ### out of the response for speaking and using it to control the robot
                                
                processedResponse, commandSequence = utils.process_commands(assistant_response)

                if commandSequence != []:
                    utils.color_printer("red", str(commandSequence))

                if self.voice_on:
                    self.text_instance.speak_text(processedResponse)
        else:
            print("No text collected")

        return assistant_response
       

    def run_robot_demo(self):
        """ run the demo """

        self.intialize_core()

        i = 0
        while (i < self.iteration_count):

            if self.speech_instance.get_speech_text():

                self.run_one_cycle(self.speech_instance.get_collected_text())
                i += 1
                print("Iteration: " + str(i))
        
        
        self.text_instance.speak_text("This is the end of the demo, thank you for using the demo today.")

if __name__ == "__main__":

    demo_instance = full_cycle_demo(robot_prompt, 
                                    voice_on= True, 
                                    max_tokens = robot_max_tokens, 
                                    iteration_count = robot_iteration_count, 
                                    generate_sensor_data = None)

    demo_instance.run_robot_demo()