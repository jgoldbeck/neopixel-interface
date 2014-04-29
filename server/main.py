#!/usr/bin/env python
from twisted.internet import reactor, task, threads
from txosc import osc
from txosc import dispatch
from txosc import async
import re
from datetime import datetime
import time

global reset
reset = False

leds = file('/dev/spidev0.0', 'wb')
nleds = 160
nzeros = 5
global buff
global blueness
blueness = 0

buff = bytearray(nleds*3)
zeros = bytearray(nzeros)

class UDPReceiverApplication(object):
    def __init__(self, port):
        self.port = port
        self.receiver = dispatch.Receiver()
        self._server_port = reactor.listenUDP(self.port, async.DatagramServerProtocol(self.receiver))
        print("Listening on osc.udp://localhost:%s" % (self.port))

        # Simple
        # self.receiver.addCallback("/1/fader1", self.hue_handler)
        # self.receiver.addCallback("/1/fader2", self.saturation_handler)
        # self.receiver.addCallback("/1/fader3", self.intensity_handler)
        # self.receiver.addCallback("/1/fader4", self.offset_handler)
        # self.receiver.addCallback("/1/fader5", self.speed_handler)
        # self.receiver.addCallback("/2/*", self.mode_handler)

        # # Beat Machine
        # self.receiver.addCallback("/3/rotary1", self.hue_handler)
        # self.receiver.addCallback("/3/rotary2", self.saturation_handler)
        # self.receiver.addCallback("/3/rotary3", self.intensity_handler)

        # Pillow Room
        # self.receiver.addCallback("/*", self.mode_page_handler)
        self.receiver.addCallback("/uniform/*", self.uniform_handler)
        # self.receiver.addCallback("/rainbow/*", self.rainbow_handler)
        # self.receiver.addCallback("/wheel/*", self.wheel_handler)
        # self.receiver.addCallback("/fade/*", self.fade_handler)
        # self.receiver.addCallback("/inertial_random/*", self.inertial_random_handler)


        # fallback:
        # self.receiver.fallback = self.fallback



    def uniform_handler(self, message, address):
        global blueness
        if message.getValues()[0]:
            change = + 1
        else:
            change = - 1
        blueness = (blueness + change) % 128


def get_path(message):
    return str(message).split(' ')[0]

def get_page(message):
    path = get_path(message)
    return path.split('/')[1]

def get_element(message):
    path = get_path(message)
    return path.split('/')[2]

def get_number(message):
    element_string = get_element(message)
    print element_string
    element_number = int(re.sub(r'\D', '', element_string))

    return element_number


def computeBuffer(redness_array):
    for i in range(nleds):
        buff[3*i] = 128
        buff[3*i+1] = 128+redness_array[0]
        buff[3*i+2] = 128+int (blueness)
    redness_array[0] = (redness_array[0] + 1) % 128
    writeBuffer(buff) # sync
    # threads.deferToThread(writeBuffer, buff) # async


def writeBuffer(buff):
    # print (buff[0], buff[1], buff[2] )
    leds.write(buff+zeros)
    leds.flush()


task.LoopingCall(computeBuffer, [0]).start(.03)

modes = [None, 'u', 'r', 'R', 'w', 'f']

if __name__ == "__main__":
    app = UDPReceiverApplication(8000)
    reactor.run()
