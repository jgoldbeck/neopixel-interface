#!/usr/bin/python

from twisted.internet import reactor, task, threads
from txosc import dispatch
from txosc import async
import numpy as np
import Image

spidev = file('/dev/spidev0.0', 'wb')

class TwistedPuddle(object):
    def __init__(self, port):
        self.port = port
        self.receiver = dispatch.Receiver()
        self._server_port = reactor.listenUDP(self.port, async.DatagramServerProtocol(self.receiver))
        print("Listening on osc.udp://localhost:%s" % (self.port))

        self.nleds = 160
        self.threshold = 2.
        self.buff = bytearray(self.nleds*3)
        for i in range(len(self.buff)):
            self.buff[i] = 0x80
        self.zeros = bytearray(5)
        self.spokes = []
        for i in range(8):
            self.spokes.append([-1 for j in range(20)])
        self.launchpad = [bytearray([0x80,0x80,0x80])]*8
        self.colorTable = self.generateColorTable()

        # LED output loop
        task.LoopingCall(self.mainLoop).start(.03)

        # all top level osc commands
        self.receiver.addCallback("/*", self.handleOSC)

    def colorMap(self,value):
        index = int((value-self.threshold)*32)
        if index > 255:
            index=255
        return self.colorTable[index*3:index*3+3]

    def handleOSC(self, message, address):
        arg = message.getValues()
        for i in range(8):
            if arg[i] >= self.threshold:
                self.launchpad[i] = self.colorMap(arg[i])
            else:
                self.launchpad[i] = bytearray([0x80,0x80,0x80])

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
        im = Image.open('hue-saturation-gradient.png').convert('RGB')
        height = im.size[1]
        pixel_strip = im.load()
        pixel_list = [pixel_strip[x, x] for x in range(height)]
        print pixel_list
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
