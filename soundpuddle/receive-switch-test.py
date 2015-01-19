#!/usr/bin/python

from twisted.internet import reactor, task, threads
from txosc import dispatch
from txosc import async
import numpy as np
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

        self.switch_position = None
        task.LoopingCall(self.mainLoop).start(.03)


        self.receiver.addCallback("/main", self.handleSwitch)

        # TO-DO, don't respond to switch, only to pd
        self.receiver.addCallback("/*", self.handleOSC)


    def handleSwitch(self, message, address):
        arg = message.getValues()
        print 'Received main signal'
        self.switch_position = arg[0]

    def handleOSC(self, message, address):
        arg = message.getValues()

    def mainLoop(self):
        nleds = 160
        nzeros = 5

        if (self.switch_position):
            r, g, b = 20, 0, 0
        else:
            r, g, b = 0, 0, 0

        buff = bytearray(nleds*3)
        for i in range(nleds):
            buff[3*i] = 128+g
            buff[3*i+1] = 128+r
            buff[3*i+2] = 128+b

        zeros = bytearray(nzeros)

        spidev.write(buff+zeros)

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
