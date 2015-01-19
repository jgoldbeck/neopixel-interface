#! /usr/bin/env python

from twisted.internet import reactor, task
from txosc import osc
from txosc import dispatch
from txosc import async
# import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BCM)

# GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

class SwitchSend(object):
    def __init__(self, port, host="127.0.0.1"):
        self.port = port
        self.host = host
        self.client = async.DatagramClientProtocol()
        self._client_port = reactor.listenUDP(0, self.client)
        self.switchValue = 1
        # LED output loop
        # task.LoopingCall(self.checkSwitch).start(.1)
        task.LoopingCall(self.sendSwitch).start(1) # in case of pi reboot or signal drop send this regularly

    def checkSwitch(self):
        self.switchValue = GPIO.input(17)
        self.sendSwitch() # to-do only do this in case of change

    def sendSwitch(self):
        self.client.send(osc.Message("/main", self.switchValue), (self.host, self.port))

if __name__ == "__main__":
    app = SwitchSend(8666)
    reactor.run()

# GPIO.cleanup()
