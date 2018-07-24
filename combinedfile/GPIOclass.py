
import RPi.GPIO as GPIO
import time

class GPIOclass():

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pin = 0
        self.ifSetup = False
        self.pinState = False 
        self.outputstring = "pin isn't setup"
    
    def perform(self, phrase):
        if phrase == "on":
            self.output(1)
        elif phrase == "off":
            self.output(0)
        elif phrase == "status":
            self.status()
        else:
            self.setupPin(phrase)
        return self.outputstring
    def checkPinState(self):
        self.pinState = GPIO.input(self.pin)
        return self.pinState
    def setupPin(self, number):
        #see if number is available on GPIO setup
        if 2 <= number <= 27:
            self.pin = number
            GPIO.setup(self.pin, GPIO.OUT)
            self.ifSetup = True
            self.outputstring = "pin activated"
        else:
            self.outputstring = "pin not available"
    def output(self, state):
        if self.ifSetup:
            GPIO.output(self.pin, state)
            self.pinState = state
            self.status()
        else:
            self.outputstring = "pin isn't setup"
    def checkIfSetup(self):
        return self.ifSetup
    def status(self):
        if self.ifSetup:
            if self.pinState:
                self.outputstring = "pin is on"
            else:
                self.outputstring = "pin is off"
        else:
            self.outputstring = "pin isn't setup"
    def returnOutputString(self):
        return self.outputstring


