20141009
--------

Put these 2 lines in /etc/rc.local

sudo -H -E screen -d -m /home/ccrma/rainbow-starfish/soundpuddle/adaptiveQuiet.py
sudo -H -E -u ccrma screen -d -m pd -nogui -audiodev 3 -channels 1 -nodac -audiobuf 15 /home/ccrma/rainbow-starfish/soundpuddle/main.pd
