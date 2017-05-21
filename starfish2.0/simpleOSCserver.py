#!/usr/bin/env python

import liblo, sys

if len(sys.argv)>=2:
    port = int(sys.argv[1])
else:
    print 'please supply port number!'
    sys.exit(1)

def handleMsg(pathstr, arg, typestr, server, usrData):
    print pathstr, arg, len(arg)

server = liblo.Server(port)
server.add_method(None, None, handleMsg)
while True:
    server.recv(1)
