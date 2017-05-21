#!/usr/bin/python

from twisted.internet import reactor, task, threads
from txosc import dispatch
from txosc import async
import numpy as np
from itertools import chain
# import Image
import math
import random
import os

try: # in case spidev not connected
    spidev  = file('/dev/spidev0.0', "wb")
    spi_connected = True
except:
    print 'SPIDEV not connected'
    spi_connected = False

class TwistedPuddle(object):
    def __init__(self, port):
        self.port = port
        self.receiver = dispatch.Receiver()
        self._server_port = reactor.listenUDP(self.port, async.DatagramServerProtocol(self.receiver))
        print("Listening on osc.udp://localhost:%s" % (self.port))

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

        # sparkle 2.0 additional magic numbers
        self.location_boost = 0.3;
        self.hue_rotate_speed = 0.5;
        self.hue_amplitude = 12;


        ## colors
        self.off_white = bytearray([170, 190, 160]) # g, r, b
        self.black = bytearray([128, 128, 128]) # g, r, b

        self.led_map = [[0] * self.leds_per_spoke for x in range(self.nspokes)]
        self.spoke_sparkle_fade_randomness = 0
        self.hue = 0
        self.hue_shifter = [0, 0, 0]

        self.threshold = 0.
        self.soundVals = [0] * self.nspokes
        self.buff = bytearray(self.nleds*3)
        self.frameLength = .05
        for i in range(len(self.buff)):
            self.buff[i] = 0x80
        self.zeros = bytearray(5)
        self.launchpad = [bytearray([0x80,0x80,0x80])]*8
        # self.colorTable = self.generateColorTable()
        self.adaptiveThreshold = [0.] * 24
        self.quietTime = 0
        self.lastArg = [0, 0]
        self.maxArgSum=[0,0]

        # LED output loop
        task.LoopingCall(self.mainLoop).start(self.frameLength)

        # all top level osc commands
        self.receiver.addCallback("/*", self.handleOSC)


    def handleOSC(self, message, address):
        arg = message.getValues()
        # self.launchpad = [bytearray([0x80,0x80,0x80])]*8
        for i in range(0, self.nspokes):
            v = arg[i*3] + arg[i*3+1] + arg[i*3+2]
            value = math.log10(v*self.amplification + 0.0000000000000000001)

            self.soundVals[i] = value



    def setLedMapFromSoundVals(self): # magic numbers!
        value = self.soundVals[0]
        threshold = self.adaptiveThreshold[0]

        if (value > 0):
            sparkle_fraction = self.sparkle_fraction * (1 + self.sparkle_fraction_amplification * (value - threshold + self.sparkle_fraction_music_correction))
        else:
            sparkle_fraction = self.sparkle_fraction

        sparkle_length = self.sparkle_length
        new_sparkle_fraction = sparkle_fraction / sparkle_length
        match = sparkle_length - 1

        for spoke_num in range(self.nspokes):
            for i in range(self.leds_per_spoke):
                s = random.random()

                bonus = (i < self.leds_per_spoke - 1 and not self.led_map[spoke_num][i]) and (self.location_boost * ((self.led_map[spoke_num][i+1] is match) and 1))
                s -= bonus

                if (s < new_sparkle_fraction):
                    self.led_map[spoke_num][i] += self.sparkle_length

        self.spoke_sparkle_fade_randomness = value * self.sparkle_fade_randomness_amplification if value > 0 else 0

        self.adaptiveThreshold[0] = max(threshold - self.threshold_decay, value)

    def rotateHue(self):
        self.hue += self.hue_rotate_speed
        self.hue %= 360
        rads = self.hue / 360.0 * 2.0 * math.pi
        self.hue_shifter = [int(self.hue_amplitude * math.sin(rads)), int(self.hue_amplitude * math.sin(rads + math.pi * 2 / 3)), int(self.hue_amplitude * math.sin(rads + math.pi * 4 / 3))]

    def darkenLedMap(self):
        for spoke_num in range(self.nspokes):
            for i in range(self.leds_per_spoke):
                self.led_map[spoke_num][i] = max(0, self.led_map[spoke_num][i] - 1)

    def setBufferFromLedMap(self):
        starting_color = bytearray([min(self.off_white[k] + self.hue_shifter[k], 255) for k in range(3)])
        # print starting_color[0],  starting_color[1],  starting_color[2]
        linear_led_map = chain.from_iterable([ind%2 and x[::-1] or x for ind, x in enumerate(self.led_map)])
        for led_idx, led_val in enumerate(linear_led_map):
            if (led_val):
                for k in range(3):
                    self.buff[led_idx * 3 + k] = starting_color[k]
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
        self.rotateHue()
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
    app = TwistedPuddle(8666)
    reactor.run()
