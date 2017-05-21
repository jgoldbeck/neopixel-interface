#!/usr/bin/python

import numpy as np
# import Image
import math
import random
import os
import threading

try: # in case spidev not connected
    spidev  = file('/dev/spidev0.0', "wb")
    spi_connected = True
except:
    print 'SPIDEV not connected'
    spi_connected = False

def setInterval(func, time):
    e = threading.Event()
    while not e.wait(time):
        func()

class LEDLoop(object):
    def __init__(self):
        self.nleds = 160
        self.nspokes = 8
        self.leds_per_spoke = self.nleds / self.nspokes

        ## sparkle magic numbers ##
        self.sparkle_fraction = 0.05
        self.sparkle_fraction_amplification = 2.5 # music responsive
        self.sparkle_length = 3
        self.sparkle_fade_rate = 0.4 # non-music responsive
        self.sparkle_fade_randomness_amplification = 0.6 # music responsive
        self.sparkle_fraction_music_correction = 0.09
        self.brightness_min = 7 # prevents the final color in the fade from being strongly colored when quiet
        self.amplification = 250.
        self.threshold_decay = .2


        ## colors
        self.off_white = bytearray([170, 190, 160]) # g, r, b
        self.off_green = bytearray([240, 160, 135]) # g, r, b
        self.black = bytearray([128, 128, 128]) # g, r, b

        self.led_map = [0] * self.nleds
        self.spoke_sparkle_fade_randomness = 0

        self.threshold = 0.
        self.soundVals = [0] * self.nspokes
        self.buff = bytearray(self.nleds*3)
        self.frameLength = .03
        for i in range(len(self.buff)):
            self.buff[i] = 0x80
        self.zeros = bytearray(5)
        self.launchpad = [bytearray([0x80,0x80,0x80])]*8
        # self.colorTable = self.generateColorTable()
        self.adaptiveThreshold = [0.] * 24
        self.quietTime = 0
        self.lastArg = [0, 0]
        self.maxArgSum=[0,0]

  


    def setLedMapFromSoundVals(self): # magic numbers!
        value = 1
        threshold = self.adaptiveThreshold[0]

        if (value > 0):
            sparkle_fraction = self.sparkle_fraction * (1 + self.sparkle_fraction_amplification * (value - threshold + self.sparkle_fraction_music_correction))
        else:
            sparkle_fraction = self.sparkle_fraction

        sparkle_length = self.sparkle_length
        new_sparkle_fraction = sparkle_fraction / sparkle_length
        for i in range(self.nleds):
            if (random.random() < new_sparkle_fraction):
                self.led_map[i] += self.sparkle_length

        self.spoke_sparkle_fade_randomness = value * self.sparkle_fade_randomness_amplification if value > 0 else 0

        self.adaptiveThreshold[0] = max(threshold - self.threshold_decay, value)



    def darkenLedMap(self):
        self.led_map[:] = [max(0, x - 1) for x in self.led_map]

    def setBufferFromLedMap(self):
        for led_idx, led_val in enumerate(self.led_map):
            if (led_val):
                for k in range(3):
                    self.buff[led_idx * 3 + k] = self.off_green[k]
            elif (self.buff[led_idx * 3] is 128 and self.buff[led_idx * 3 + 1] is 128 and self.buff[led_idx * 3 + 2] is 128):
               continue
            elif (sum(self.buff[led_idx * 3:led_idx * 3 + 3]) < (128 * 3) + self.brightness_min):
                self.buff[led_idx * 3:led_idx * 3 + 3] = self.black
            else:
                sparkle_fade_randomness = self.spoke_sparkle_fade_randomness
                for k in range(3):
                    sparkle_fade_rate = max(0, self.sparkle_fade_rate * (1 + sparkle_fade_randomness * (random.random() - .5)))
                    self.buff[led_idx * 3 + k] = int((self.buff[led_idx * 3 + k] - 128) * math.exp(-1 * sparkle_fade_rate) + 128)

    def writeBuffer(self):
        if (spi_connected):
            spidev.write(self.buff+self.zeros)
            spidev.flush()

    def mainLoop(self):
        self.darkenLedMap()
        self.setLedMapFromSoundVals()
        self.setBufferFromLedMap()
        self.writeBuffer()


# TwistedOSC utility functions
def get_path(message):
    return str(message).split(' ')[0]

def get_page(message):
    path = get_path(message)
    return path.split('/')[1]

def get_element(message):
    path = get_path(message)
    return path.split('/')[2]

def get_number(message): # not value, but number of slider or wheel
    element_string = get_element(message)
    print element_string
    element_number = int(re.sub(r'\D', '', element_string))
    return element_number



# Start server
if __name__=='__main__':
    app = LEDLoop()
    setInterval(app.mainLoop,.05)
