
import RPi.GPIO as GPIO
import time

class GPIOclass():

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pins = [] 
        self.outputstring = "pin isn't setup"
    
    def perform(self, action, numLights):
        if action == "on":
            self.output(numLights, 1)
        elif action == "off":
            self.output(numLights, 0)
        elif action == "status":
            self.status(numLights)
        return self.outputstring
    def setup(self, phrase, numbers):
        self.outputstring = ""
        if phrase == "new":
            self.setupPin(numbers)
        else:
            for num in numbers:
                if self.ifSetup(num):
                    self.outputstring += "pin %s removed " %num
                    self.pins.remove(num)
                else:
                    self.outputstring += "pin %s was never setup "%num
        return self.outputstring
    def setupPin(self, numbers):
        #see if number is available on GPIO setup
        for num in numbers:
            if self.ifSetup(num):
                self.outputstring += "pin %s already taken "%num
            elif 4 <= num <= 27:
                self.pins.append(num)
                GPIO.setup(num, GPIO.OUT)
                self.outputstring += "pin %s activated as light %s " %(num, len(self.pins))
            else:
                self.outputstring += "pin %s not available " %num 
    def output(self, numLights, state):
        self.outputstring = ""
        if len(self.pins) < 1:
            self.outputstring = "no pins setup"
            return
        for light in numLights:
            if light  == "all":
                for x in self.pins:
                    GPIO.output(x, state)
                self.outputstring += "all lights turned %s" %self.checkState(self.pins[0])
                return
            if len(self.pins)>=light:
                GPIO.output(self.pins[light-1], state)
                if state:
                    self.outputstring += "light %s turned on " %light
                else: 
                    self.outputstring += "light %s turned off " %light
            else:
                self.outputstring += "light %s isn't available "%light
    def ifSetup(self, num):
        if num in self.pins:
            return True
        else:
            return False
    def checkState(self, pin):
        state = GPIO.input(pin)
        if state:
            return "on"
        else:
            return "off"
    def status(self, numLights):
        self.outputstring = ""
        for light in numLights:
            if len(self.pins)>0:
                if light == "all":
                    for x in range(0, len(self.pins)):
                        self.outputstring += "light %s pin %s is %s||" %(x+1, self.pins[x], self.checkState(self.pins[x]))
                else:
                    try:
                        self.outputstring += "light %s pin %s is %s " %(light, self.pins[light-1], self.checkState(self.pins[light-1]))
                    except IndexError:
                        self.outputstring += "light %s isn't setup " %light
            else:
                self.outputstring = "no pins are setup"
    def returnOutputString(self):
        return self.outputstring


