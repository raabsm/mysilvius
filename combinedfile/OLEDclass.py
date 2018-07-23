import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

RST = None     # on the PiOLED this pin isnt used
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = -2
top = padding
bottom = height-padding
x = 0 
font = ImageFont.load_default()

class OLEDclass():

    def __init__(self):

        draw.text((x, top), "initialized", font=font, fill=255)
        disp.image(image)
        disp.display()

    def printToOLED(self, result):
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        if len(result) > 20:
            cut = result[0:21]
            draw.text((x, top), cut, font=font, fill=255)
            draw.text((x, top+8), result[21:], font=font, fill=255)
        else:
            draw.text((x, top), result, font=font, fill=255) 

        #draw.text((x, top+20), status, font=font, fill=255)
        disp.image(image)
        disp.display()
    def printStatus(self, status):
        draw.text((x, top+18), status, font=font, fill=255)
        disp.image(image)
        disp.display()
