#! /usr/bin/env python

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

while True:
    if(GPIO.input(17) == 0):
        print("Off")
    else:
        print("On")

GPIO.cleanup()
