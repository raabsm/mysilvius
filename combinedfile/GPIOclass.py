
import RPi.GPIO as GPIO
import time

class GPIOclass():

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pins = [] 
        self.outputstring = "pin isn't setup"
    
    def perform(self, numLight, action):
        if action == "on":
            self.output(numLight, 1)
        elif action == "off":
            self.output(numLight, 0)
        elif action == "status":
            self.status(numLight)
        return self.outputstring
    def setup(self, phrase, num):
        if phrase == "new":
            self.setupPin(num)
        else:
            if self.ifSetup(num):
                self.outputstring = "pin %s light %s removed" %(num, self.pins.index(num) + 1)
                self.pins.remove(num)
            else:
                self.outputstring = "pin was never setup"
        return self.outputstring
    def setupPin(self, number):
        #see if number is available on GPIO setup
        if self.ifSetup(number):
            self.outputstring = "pin already taken"
        elif 2 <= number <= 27:
            self.pins.append(number)
            GPIO.setup(number, GPIO.OUT)
            self.outputstring = "pin %s activated as light %s" %(number, len(self.pins))
        else:
            self.outputstring = "pin not available"
    def output(self, numLight, state):
        if numLight == "all" and len(self.pins) > 0:
            for x in self.pins:
                GPIO.output(x, state)
            self.outputstring = "all lights turned %s" %self.checkState(self.pins[0])
            return
        if len(self.pins)>=numLight:
            GPIO.output(self.pins[numLight-1], state)
            if state:
                self.outputstring = "light %s turned on" %numLight
            else: 
                self.outputstring = "light %s turned off" %numLight
        else:
                self.outputstring = "That light isn't available"
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
    def status(self, numLight):
        self.outputstring = ""
        if len(self.pins)>0:
            if numLight == "all":
                for x in range(0, len(self.pins)):
                    self.outputstring += "light %s pin %s is %s||" %(x+1, self.pins[x], self.checkState(self.pins[x]))
            else:
                try:
                    self.outputstring += "light %s pin %s is %s" %(numLight, self.pins[numLight-1], self.checkState(self.pins[numLight-1]))
                except IndexError:
                    self.outputstring = "aren't that many lights setup"
        else:
            self.outputstring = "pins aren't setup"
    def returnOutputString(self):
        return self.outputstring


