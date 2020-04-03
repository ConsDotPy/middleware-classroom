#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
from mfrc522 import SimpleMFRC522


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
reader = SimpleMFRC522()
led = 4
GPIO.setup(led, GPIO.OUT)
def WriteRFID(text):
    GPIO.setmode(GPIO.BCM)
    try:
	    print("Colocar tarjeta para escribir...")
	    GPIO.output(led,1)
	    reader.write(text)
	    print("Dato escrito...")
	    GPIO.output(led,0)
    except:
	    GPIO.cleanup()
def ReadRFID():
    GPIO.setmode(GPIO.BCM)
    try:
	    print("Colocar tarjeta...")
	    GPIO.output(led, 1)
	    id, text = reader.read()
	    GPIO.output(led, 0)
	    print(id, text)
	    return id, text
    except:
       		 GPIO.cleanup()
