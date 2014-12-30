#!/usr/bin/python

from twisted.internet import reactor, task, threads
from txosc import dispatch
from txosc import async
import numpy as np
import Image
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
        self.led_map = [0] * self.nleds
        self.threshold = 0.
        self.amplification = 128.
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

        # LED output loop
        task.LoopingCall(self.mainLoop).start(self.frameLength)

        # all top level osc commands
        self.receiver.addCallback("/*", self.handleOSC)


    # def probabiliticWhite(self,value):
    #     if (value > random.uniform(0, 3)): # magic number in here for now
    #         return [0xFF, 0xFF, 0xFF] # white
    #     else:
    #         return [0x80, 0x80, 0x80] # black

    def handleOSC(self, message, address):
        arg = message.getValues()
        # self.launchpad = [bytearray([0x80,0x80,0x80])]*8

        if arg[0] + self.lastArg[0] + arg[1] + self.lastArg[1] > .020:
            self.quietTime = 0
        else:
            self.quietTime += 1

        self.lastArg[0] = arg[0]
        self.lastArg[1] = arg[1]

        if self.quietTime < 30/self.frameLength: # one second
            for i in range(0, self.nspokes):
                v = arg[i*3] + arg[i*3+1] + arg[i*3+2]
                value = math.log10(v*self.amplification)
                threshold = self.adaptiveThreshold[i]
                for j in range(0, self.leds_per_spoke):
                    self.led_map[i + self.nspokes * j] += random.expovariate(1)

                # if value >= threshold:
                #     for j in range(0, self.leds_per_spoke):
                #         self.led_map[i + self.nspokes * j] += random.uniform(0, max((value - threshold), 2)) # magic number here
                        # self.buff[3 * k], self.buff[3 * k + 1], self.buff[3 * k + 2] = self.probabiliticWhite(3*(value - threshold));
                self.adaptiveThreshold[i] = max(threshold - .02, value)
        self.darkenLedMap()


    # def shiftSpokes(self):
    #     for i in range(4):
    #         self.buff[(60*2*i):(60*2*i+60)] = self.launchpad[2*i] + self.buff[(60*2*i):(60*2*i+57)]
    #         self.buff[(60*(2*i+1)):(60*(2*i+1)+60)] = self.buff[(60*(2*i+1)+3):(60*(2*i+1)+60)] + self.launchpad[2*i+1]

    def darkenLedMap(self):
        self.led_map[:] = [max(0, x - 1) for x in self.led_map]

    def setBufferFromLedMap(self):
        for led_idx, led_val in enumerate(self.led_map):
            for k in range(3):
                self.buff[led_idx * 3 + k] = 0xFF if led_val else 0x80

    def writeBuffer(self):
        if (spi_connected):
            spidev.write(self.buff+self.zeros)
            spidev.flush()

    def mainLoop(self):
        # self.shiftSpokes()
        self.setBufferFromLedMap()
        self.writeBuffer()

    # def generateColorTable(self):
    #     im = Image.open(os.path.join(os.path.dirname(__file__), 'unfull_pastel.png')).convert('RGB')
    #     height = im.size[1]
    #     pixel_strip = im.load()
    #     pixel_list = [pixel_strip[x, x] for x in range(height)]
    #     gamma = bytearray(256)
    #     for i in range(256):
    #         gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)

    #     column = [0 for x in range(height)]
    #     column = bytearray(height * 3 + 1)

    #     for y in range(height):
    #         value = pixel_list[y]
    #         y3 = y * 3
    #         column[y3]     = gamma[value[1]]
    #         column[y3 + 1] = gamma[value[0]]
    #         column[y3 + 2] = gamma[value[2]]
    #         print (column[y3],column[y3+1],column[y3+2])

    #     return column



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
