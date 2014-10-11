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
    opt.add_option("-w","--wait",action="store",type="int",dest="wait_time",default=10,
                   help="how many seconds to wait between each get() (default 10)")
    (options,args) = opt.parse_args()

    conn = Connection(options.host)
    channel = Channel(conn)

    queue = channel.queueDeclare()
    print("queue name is "+queue)
    channel.queueBind(queue,"amq.direct","mtk_test")

    print("press ctrl-C to exit")
    while keep_running:
        i = 0
        while i < options.wait_time and keep_running:
            time.sleep(1)
            i += 1
        if keep_running:
            print("getting..")
            message_count = 1 # to prime things
            while message_count > 0:
                (routing_key, message_count, content) = channel.basicGet(queue)
                print("%d messages remaining" % message_count)
                print("  "+content)
    print("shutting down")

    # these three aren't necessary, but are here for testing
    channel.queueUnbind(queue,"amq.direct","mtk_test")
    channel.queueDelete(queue)

    channel.close() # isn't necessary - closing the connection will close the channel
    conn.close()    # should shutdown the connection gracefully
