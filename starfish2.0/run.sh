#!/bin/bash

pd-extended -nogui -audiodev 3 -channels 1 -nodac -audiobuf 15 main.pd &
./simpleOSCserver.py 8666 # prints OSC message path, arguments, and length to stdout
