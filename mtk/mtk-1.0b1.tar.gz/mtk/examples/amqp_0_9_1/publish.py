#!/usr/bin/env python

import optparse
import os
import signal
import ssl
import sys
import time

from mtk.amqp_0_9_1 import *

keep_running = True

def sigHandler(signal, frame):
    global keep_running
    keep_running = False

signal.signal(signal.SIGINT, sigHandler)

#######################################################################################################################

def parser():
    usage = "Usage: %prog [options]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-s","--server",default="localhost",dest="server",
                      help="the server running the messaging service")

    parser.add_option("-u","--user",dest="user",
                      help="the user to authenticate as")
    parser.add_option("-p","--password",dest="password",
                      help="the password to use to authenticate")
    parser.add_option("-k","--key",dest="keyfile",
                      help="the file containing a key")
    parser.add_option("-c","--cert",dest="certfile",
                      help="the file containing a certificate")
    parser.add_option("-a","--cacert",dest="ca_certfile",
                      help="the file containing the CA certificates")
    
    parser.add_option("-v","--vhost",default="/",dest="vhost",
                      help="the virtual host in the messaging service to connect to")
    parser.add_option("-e","--exchange",default="amq.topic",dest="exchange",
                      help="an exchange in the virtual host to publish or subscribe to")
    return parser

#######################################################################################################################

ca_cert_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"ca_certs.pem")

def connect(options):
    # port 5671 is for SSL, port 5672 is for TCP
    if options.keyfile is not None or options.certfile is not None:
        if options.keyfile is None:
            print("you must specify a key file for user with your cert file")
            sys.exit(1)
        if options.certfile is None:
            print("you must specify a cert file for user with your key file")
            sys.exit(1)
        if options.ca_certfile is None:
            print("you must specify a ca_certs file")
            sys.exit(1)
        print("connecting to %s:5671 with certificate and key" % options.server)
        return Connection(host=options.server,
                          port=5671,
                          virtual_host=options.vhost,
                          mechanism=X509Mechanism(),
                          ssl_options={"keyfile":options.keyfile,
                                       "certfile":options.certfile,
                                       "cert_reqs":ssl.CERT_REQUIRED,
                                       "ca_certs":options.ca_certfile},
                          heartbeat=60)
    if options.user is not None or options.password is not None:
        if options.password is None:
            print("you must specify a user along with a password")
            sys.exit(1)
        if options.user is None:
            print("you must specify a password along with a user")
            sys.exit(1)
        if options.ca_certfile is not None:
            print("connecting over SSL to %s:5671 with username and password" % options.server)
            return Connection(host=options.server,
                              port=5671,
                              virtual_host=options.vhost,
                              mechanism=PlainMechanism(options.user,options.password),
                              ssl_options={"cert_reqs":ssl.CERT_REQUIRED,
                                           "ca_certs":options.ca_certfile},
                              heartbeat=60)
        else:
            print("connecting over TCP to %s:5672 with username and password" % options.server)
            return Connection(host=options.server,
                              port=5672,
                              virtual_host=options.vhost,
                              mechanism=PlainMechanism(options.user,options.password),
                              heartbeat=60)
    else:
        print("connecting to %s:5672 anonymously" % options.server)
        return Connection(host=options.server,
                          port=5672,
                          virtual_host=options.vhost,
                          mechanism=PlainMechanism(),
                          heartbeat=60)

#######################################################################################################################

message_number = 1

def publish(channel, exchange):
    global message_number
    content = "message %d" % message_number
    print("publishing: %s" % content)
    channel.basicPublish(content=content,
                         exchange=exchange,
                         routing_key="test1")
    message_number += 1

#######################################################################################################################

if __name__ == "__main__":
    (options, args) = parser().parse_args()

    conn = connect(options)
    channel = conn.channel()

    channel.exchangeDeclare(exchange=options.exchange,
                            type="topic",
                            passive=False,
                            durable=False)

    print("press ctrl-C to exit")
    while keep_running:
        publish(channel,options.exchange)
        time.sleep(2)
    conn.close()
    print("shutting down")

#######################################################################################################################
