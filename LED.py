import RPi.GPIO as GPIO
from time import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
print "LED on"
GPIO.output(18,GPIO.HIGH)
prev = time()
now = prev 
while(now - prev < 3):
    now = time()
print "LED off"
GPIO.output(18,GPIO.LOW)

