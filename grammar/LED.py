import RPi.GPIO as GPIO
from time import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
print "LED on"
GPIO.output(18,True)
prev = time()
now = prev 
while(now - prev < 10):
    #test whether other commands can be said while this program is running...doesn't work 
    now = time()
print "LED off"
GPIO.output(18,False)

#this is a test comment
