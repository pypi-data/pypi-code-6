#!/usr/bin/env python

import optparse
import signal
import time

from mtk.amqp_0_9_1 import *

keep_running = True

def sigHandler(signal, frame):
    global keep_running
    keep_running = False

signal.signal(signal.SIGINT, sigHandler)

if __name__ == "__main__":
    opt = optparse.OptionParser(usage="usage: %prog [options]")
    opt.add_option("-o","--host",action="store",type="string",dest="host",default="localhost",
                   help="the host running the messaging service (default localhost)")
    (options,args) = opt.parse_args()


    conn = Connection(options.host)
    channel = conn.channel()

    channel.exchangeDeclare("mtk_test")
    
    print("press ctrl-C to exit")
    channel.txSelect()
    msg_num = 1
    while keep_running:
        print("  publish %d" % msg_num)
        channel.basicPublish("test message %d" % msg_num,
                             "amq.direct",
                             "mtk_test")
        msg_num += 1
        if msg_num % 10 == 0:
            if msg_num / 10 % 2 == 1:
                print("commit!")
                channel.txCommit()
            else:
                print("rollback!")
                channel.txRollback()
        time.sleep(1)


    channel.close()
    conn.close()
