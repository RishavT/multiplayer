from __future__ import print_function
"""
Simple program to play a file at a given timestamp.
"""

author = "Rishav Thakker (thakker.rishav@gmail.com)"

LICENSE = "GNU GPL Version 2.0"

import sys, os
import time
from pygame import mixer
from pygame.mixer import music
from multiprocessing import Process, Queue

TO_ADD = 0.0
SERVER_IP = os.environ.get("PLAY_IN_A_BIT_SERVER_IP")

def configure_time_delay():
    global TO_ADD
    total = 0
    if not SERVER_IP:
        print("PLAY_IN_A_BIT_SERVER_IP not defined."
              "Not syncing time with any server.")
        return
    for i in range(3):
        ntpdate_out = os.popen("ntpdate -q -u %s" % SERVER_IP)
        ntpdate_out = ntpdate_out.read().split('\n')[0]
        ntpdate_out = ntpdate_out.replace(",", "").split(" ")
        offset = float(ntpdate_out[ntpdate_out.index("offset")+1])
        if TO_ADD == 0:
            TO_ADD = offset
        else:
            if abs(TO_ADD) > abs(offset):
                TO_ADD = offset
    print("Setting offset = %f" % TO_ADD)

def init(fname):
    mixer.init(22050, -16, 2, 1024)
    music.load(fname)
    music.rewind()
    music.play()
    music.pause()
    music.rewind()

def play(fname, timestamp):
    init(fname)
    while (timestamp - (time.time() + TO_ADD)) > 0:
        pass
    music.unpause()
    while True:
        time.sleep(1)

if __name__ == "__main__":
    fname, timestamp = sys.argv[1:]

    timestamp = float(timestamp)
    configure_time_delay()
    play(fname, timestamp)
