#!/usr/bin/python

from twisted.internet import reactor, task, threads
from txosc import dispatch
from txosc import async
import numpy as np
import Image
import math

spidev = file('/dev/spidev0.0', 'wb')

class TwistedPuddle(object):
    def __init__(self, port):
        self.port = port
        self.receiver = dispatch.Receiver()
        self._server_port = reactor.listenUDP(self.port, async.DatagramServerProtocol(self.receiver))
        print("Listening on osc.udp://localhost:%s" % (self.port))

        self.nleds = 160
        self.threshold = 0.
        self.amplification = 128.
        self.buff = bytearray(self.nleds*3)
        self.frameLength = .03
        for i in range(len(self.buff)):
            self.buff[i] = 0x80
        self.zeros = bytearray(5)
        self.launchpad = [bytearray([0x80,0x80,0x80])]*8
        self.colorTable = self.generateColorTable()
        self.adaptiveThreshold = [0.] * 24
        self.quietTime = 0
        self.lastArg = [0, 0]
        self.maxArgSum=[0,0]

        # LED output loop
        task.LoopingCall(self.mainLoop).start(self.frameLength)

        # all top level osc commands
        self.receiver.addCallback("/*", self.handleOSC)

    def colorMap(self,value):
        index = int(value*128.)
        if index > 255:
            index=255
        return self.colorTable[index*3:index*3+3]

    def handleOSC(self, message, address):
        arg = message.getValues()
        self.launchpad = [bytearray([0x80,0x80,0x80])]*8
        self.lastArg[0] = arg[0]
        maxArgSum[0] = max(maxArgSum[0], arg[0] + self.lastArg[0])
        maxArgSum[1] = max(maxArgSum[1], arg[1] + self.lastArg[1])
        print maxArgSum
        self.lastArg[1] = arg[1]
        if arg[0] > .008:
            self.quietTime = 0
        else:
            self.quietTime += 1
        # print self.quietTime

        if self.quietTime < 30/self.frameLength: # one second
            for i in range(24):
                value = math.log10(arg[i]*self.amplification)
                threshold = self.adaptiveThreshold[i]
                if value >= threshold:
                    self.launchpad[i%8] = self.colorMap(3*(value - threshold))
                self.adaptiveThreshold[i] = max(threshold - .02, value)

    def shiftSpokes(self):
        for i in range(4):
            self.buff[(60*2*i):(60*2*i+60)] = self.launchpad[2*i] + self.buff[(60*2*i):(60*2*i+57)]
            self.buff[(60*(2*i+1)):(60*(2*i+1)+60)] = self.buff[(60*(2*i+1)+3):(60*(2*i+1)+60)] + self.launchpad[2*i+1]

    def writeBuffer(self):
        spidev.write(self.buff+self.zeros)
        spidev.flush()


    def mainLoop(self):
        self.shiftSpokes()
        self.writeBuffer()

    def generateColorTable(self):
        im = Image.open('unfull_pastel.png').convert('RGB')
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
            print (column[y3],column[y3+1],column[y3+2])

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
