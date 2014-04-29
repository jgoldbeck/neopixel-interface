#!/usr/bin/python

import liblo, time, random
import numpy as np
from pyo import midiToHz as m2h

# and the frequency bins
midiNotes = range(36,84,6) # 8 bins total
f0 = 44100./4096 # 10.76 hz
allFreqs = f0*np.arange(100) # 100 is the number of frequencies you send across, currently
freqBins = []
for m in midiNotes:
    iwhere = np.where((allFreqs>=m2h(m-3)) & (allFreqs<m2h(m+3)))
    freqBins.append(iwhere[0])

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
        self.launchpad = [[0x80,0x80,0x80]]*8

    def handleOSC(self, pathstr, arg, typestr, server, usrData):
        for i in range(8):
            if arg[i] >= self.sensitivity:
                print 'Launching: ', i
                self.launchpad[i] = self.colorMap(arg[i])
            else:
                self.launchpad[i] = [0x80,0x80,0x80]

    def colorMap(self,value):
        diff = value - self.sensitivity
        if diff<

    def shiftSpokes(self):
        for i in range(4):
            self.buff[(60*2*i):(60*2*i+60)] = self.launchpad[2*i] + self.buff[(60*2*i):(60*2*i+57)]
            self.buff[(60*(2*i+1)):(60*(2*i+1)+60)] = self.buff[(60*(2*i+1)):(60*(2*i+1)+57)] + self.launchpad[2*i+1]

    def prepareBuffer(self):
        for i in range(8):
            for j in range(20):
                if self.spokes[i][j]==1:
                    #self.buff[(i*20+j)*3:(i*20+j)*3+3] = random.choice(self.colorSet)
                    self.buff[(i*20+j)*3:(i*20+j)*3+3] = [0xFF,0xFF,0xFF]
                else:
                    self.buff[(i*20+j)*3:(i*20+j)*3+3] = [0x80,0x80,0x80]

    def writeBuffer(self):
        spidev.write(self.buff+self.zeros)
        spidev.flush()

    def mainLoop(self):
        while True:
            self.OSCserver.recv(1)
            self.shiftSpokes()
            self.prepareBuffer()
            self.writeBuffer()

if __name__=='__main__':
    sp = SoundPuddle()
    sp.mainLoop()   
