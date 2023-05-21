# Raphael Fortuna (raf269) 
# Rabail Makhdoom (rm857) 
# Final Project Report
# Lab 403, Lab Section:  4:30pm-7:30pm on Thursdays 

colors = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m"
}

class ColorText:
    """ used to print text in color """

    def __init__(self, color):
        self.colorID = colors[color]
        self.reset = colors["reset"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.colorID
        del self.reset

    def print(self, text):
        """ print text in color """
        print(self.colorID + text + self.reset)


def color_printer(color, text):
    """ print single line in color """

    with ColorText(color) as colorPrinter:
        colorPrinter.print(text)

# Usage:
# with ColorText("yellow") as colorPrinter:
#     colorPrinter.print("This text is in yellow!")

# print("This text is back to the default color.")

# robot commands
commandList = [
    "stop(",
    "moveForward(",
    "moveBackward(",
    "turnLeft(",
    "turnRight("
    ]


def process_commands(text_in):
    """ process the ### command ### out of the response """
    if "###" in text_in:
        # split the text up
        split_text = text_in.split("###")

        # commands are sent to the robot in the form of a list of dictionaries
        commandSequence = []

        # the speech sequence is the text that is spoken by the robot
        speechSequence = ""

        for phrase in split_text:

            # if the phrase is a valid command
            validCommand = False
            for command in commandList:

                # check if command is found
                if command in phrase:

                    # get the argument
                    argument = phrase.split("(")[1]
                    if len(argument) == 1: # no argument
                        argument = ""

                    else: # argument found
                        argument = argument.split(")")[0]
                        
                    commandSequence.append({command[:-1]: argument})
                    validCommand = True
                    break
                
            # if the phrase is not a valid command, add it to the speech sequence
            if not validCommand:
                speechSequence += phrase

        return speechSequence, commandSequence
    
    return text_in, []