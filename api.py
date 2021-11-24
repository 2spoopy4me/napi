from flask import Flask
import psutil
from pprint import pprint as p
import json
import threading
import time
from collections import deque

import psutil

from gup_down import *



def calc_ul_dl(rate, dt=3, interface="en0"):
    t0 = time.time()
    counter = psutil.net_io_counters(pernic=True)[interface]
    tot = (counter.bytes_sent, counter.bytes_recv)

    while True:
        last_tot = tot
        time.sleep(dt)
        counter = psutil.net_io_counters(pernic=True)[interface]
        t1 = time.time()
        tot = (counter.bytes_sent, counter.bytes_recv)
        ul, dl = [
            (now - last) / (t1 - t0) / 1000.0
            for now, last in zip(tot, last_tot)
        ]
        rate.append((ul, dl))
        t0 = time.time()


def print_rate(rate):
    try:
        print("UL: {0:.0f} kB/s / DL: {1:.0f} kB/s".format(*rate[-1]))
    except IndexError:
        "UL: - kB/s/ DL: - kB/s"


# Create the ul/dl thread and a deque of length 1 to hold the ul/dl- values
transfer_rate = deque(maxlen=1)
t = threading.Thread(target=calc_ul_dl, args=(transfer_rate,))

# The program will exit if there are only daemonic threads left.
t.daemon = True
t.start()














app = Flask(__name__)

@app.route('/interfaces/', methods=['GET'])

def get_interfaces():
    '''Returns JSON output of system's network interfaces'''
    interfaces = psutil.net_if_addrs()
    return json.dumps( list(interfaces.keys()) )


@app.route('/interfaces/en0/speed/', methods=['GET'])

def get_up_down():
    '''Returns JSON output of system's network interfaces'''
    return network_traffic()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)