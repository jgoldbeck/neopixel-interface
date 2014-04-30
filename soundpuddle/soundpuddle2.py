#!/usr/bin/python

import liblo, time, random
import numpy as np
from colorTable2 import colorTable

spidev = file('/dev/spidev0.0', 'wb')

class SoundPuddle():

    def __init__(self):
        self.nleds = 160
        self.sensitivity = 1.
        self.OSCserver = liblo.Server(8666)
        self.OSCserver.add_method(None, None, self.handleOSC)
        self.buff = bytearray(self.nleds*3)
        for i in range(len(self.buff)):
            self.buff[i] = 0x80
        self.zeros = bytearray(5)
        self.spokes = []
        for i in range(8):
            self.spokes.append([-1 for j in range(20)])
        self.launchpad = [bytearray([0x80,0x80,0x80])]*8
        self.colorTable = colorTable

    def colorMap(self,value):
        print value
        index = int((value-self.sensitivity)*32)
        if index > 255:
            index=255
        print index
        return self.colorTable[index*3:index*3+3]

    def handleOSC(self, pathstr, arg, typestr, server, usrData):
        for i in range(8):
            if arg[i] >= self.sensitivity:
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
        while True:
            self.OSCserver.recv(1)
            self.shiftSpokes()
            self.writeBuffer()
            time.sleep(0.03)

if __name__=='__main__':
    sp = SoundPuddle()
    sp.mainLoop()   
