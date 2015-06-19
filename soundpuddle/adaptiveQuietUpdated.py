#!/usr/bin/python

from twisted.internet import reactor, task, threads
from txosc import dispatch
from txosc import async
import numpy as np
from PIL import Image
import math
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

        self.nleds = 240
        self.lengthNumber = 90
        self.threshold = 0.
        self.amplification = 128.
        self.gradientFiles = [
            'golden.png',
            'orange.png',
            'pink_to_yellow.png',
            'unfull_pastel.png',
            'redder_pastel.png',
            'purple_to_blue.png'
        ]
        self.currentGradientFileIndex = 0;
        self.gradientFileName = self.gradientFiles[0];

        self.buff = bytearray(self.nleds*3)
        self.frameLength = .03
        self.colorLength = 60 * 15
        for i in range(len(self.buff)):
            self.buff[i] = 0x80
        self.zeros = bytearray(5)
        self.launchpad = [bytearray([0x80,0x80,0x80])]*8
        self.colorTable = self.generateColorTable()
        self.adaptiveThreshold = [0.] * 24
        self.quietTime = 0
        self.lastArg = [0, 0]
        self.maxArgSum = [0,0]

        # LED output loop
        self.outputLoop = task.LoopingCall(self.mainLoop)

        # On Off loop
        self.onOffLength = 999999999 # currently, forever
        self.loopOn = True;
        task.LoopingCall(self.onOffLoop).start(self.onOffLength)

        # Color file loop
        task.LoopingCall(self.colorLoop).start(self.colorLength)

        # all top level osc commands
        self.receiver.addCallback("/*", self.handleOSC)

    def colorLoop(self):
        self.colorTable = self.generateColorTable()
        self.currentGradientFileIndex = (self.currentGradientFileIndex + 1) % len(self.gradientFiles)
        self.gradientFileName = self.gradientFiles[self.currentGradientFileIndex];

    def onOffLoop(self):
        if(self.outputLoop.running):
            print 'stop'
            self.outputLoop.stop()
        else:
            print 'start'
            self.outputLoop.start(self.frameLength)

    def colorMap(self,value):
        index = int(value*128.)
        if index > 255:
            index = 255
        return self.colorTable[index*3:index*3+3]

    def handleOSC(self, message, address):
        arg = message.getValues()
        self.launchpad = [bytearray([0x80,0x80,0x80])]*8

        if arg[0] + self.lastArg[0] + arg[1] + self.lastArg[1] > .020:
            self.quietTime = 0
        else:
            self.quietTime += 1

        self.lastArg[0] = arg[0]
        self.lastArg[1] = arg[1]

        if self.quietTime < 30/self.frameLength: # one second
            for i in range(0, 8):
                v = arg[i*3] + arg[i*3+1] + arg[i*3+2]
                value = math.log10(v*self.amplification)
                threshold = self.adaptiveThreshold[i]
                if value >= threshold:
                    self.launchpad[i%8] = self.colorMap(3*(value - threshold))
                self.adaptiveThreshold[i] = max(threshold - .02, value)

    def shiftSpokes(self):


        ## Down?
        #
        # self.circ = 20;
        # print self.nleds / self.circ
        # for i in range(1, self.nleds / self.circ):
        #     print i
        #     self.buff[i*self.circ: (i+1)*self.circ] = self.buff[(i-1)*self.circ: (i)*self.circ]
        # self.buff[0:8] = self.launchpad

        # return


        # Multiple spokes

        for i in range(4): #8
            #self.buff[(self.lengthNumber*i):(self.lengthNumber*i+self.lengthNumber)] = self.launchpad[i] + self.buff[(self.lengthNumber*i):(self.lengthNumber*i+(self.lengthNumber - 3))]
            #self.buff[(self.lengthNumber*(i)):(self.lengthNumber*(i)+self.lengthNumber)] = self.buff[(self.lengthNumber*(i)+3):(self.lengthNumber*(i)+self.lengthNumber)] + self.launchpad[i]

            ## Normal (crossways)
            self.buff[(self.lengthNumber*2*i):(self.lengthNumber*2*i+self.lengthNumber)] = self.launchpad[2*i] + self.buff[(self.lengthNumber*2*i):(self.lengthNumber*2*i+(self.lengthNumber - 3))]
            self.buff[(self.lengthNumber*(2*i+1)):(self.lengthNumber*(2*i+1)+self.lengthNumber)] = self.buff[(self.lengthNumber*(2*i+1)+3):(self.lengthNumber*(2*i+1)+self.lengthNumber)] + self.launchpad[2*i+1]

            ## Down??
            # try:
            #     self.buff[(self.lengthNumber*i):(self.lengthNumber*i+self.lengthNumber)+20] = self.launchpad[i] + self.buff[(self.lengthNumber*i):(self.lengthNumber*i+(self.lengthNumber - 3))]
            # except:
            #     print 'oops'

    def writeBuffer(self):
        spidev.write(self.buff+self.zeros)
        spidev.flush()

    def mainLoop(self):
        if (spi_connected):
            self.shiftSpokes()
            self.writeBuffer()

    def generateColorTable(self):
        im = Image.open(os.path.join(os.path.dirname(__file__), self.gradientFileName)).convert('RGB')
        height = im.size[1]
        pixel_strip = im.load()
        pixel_list = [pixel_strip[x, x] for x in range(height)]
        gamma = bytearray(256)
        for i in range(256):
            gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)

        column = [0 for x in range(height)]
        column = bytearray(height * 3 + 1)

        for y in range(height):
            value = pixel_list[y]
            y3 = y * 3
            column[y3]     = gamma[value[1]]
            column[y3 + 1] = gamma[value[0]]
            column[y3 + 2] = gamma[value[2]]
            # print (column[y3],column[y3+1],column[y3+2])

        return column



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
