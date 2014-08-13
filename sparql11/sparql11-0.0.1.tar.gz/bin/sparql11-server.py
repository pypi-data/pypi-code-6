#!/usr/bin/env python3
# coding:utf-8

"""sparql11 SPARQL Endpoint"""

__author__ = "Thomas Scharrenbach"
__copyright__ = "Copyright (C) 2014 Thomas Scharrenbach"
__license__ = "Apache License v2"
__version__ = "0.0.1"

import sys

from sparql11.server import endpoint, parse_args

import logging as log

from time import sleep

import signal

root = log.getLogger()
root.setLevel(log.DEBUG)

ch = log.StreamHandler(sys.stdout)
ch.setLevel(log.DEBUG)
formatter = log.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

def signal_term_handler(signal, frame):
	"""Handle SIGTERM signal and allow graceful shutdown.

	:param signal:
	:param frame:
	:return:
	"""
	log.info('Observed SIGTERM, trying to shutdown gracefully...')
	sys.exit(0)


def main(args):
	signal.signal(signal.SIGTERM, signal_term_handler)
	args = parse_args(args=args)
	server = endpoint(dataset=args.dataset, hostname=args.hostname, port=args.port)
	log.info('Starting SPARQL Endpoint...')
	server.start()
	log.info('SPARQL Endpoint up and running.')
	try:
		while server.isAlive():
			sleep(5)
	except (KeyboardInterrupt, SystemExit):
		log.info('Interrupted')
	finally:
		log.info('Shutting down SPARQL Endpoint...')
		server.shutdown()
		log.info('Shutdown complete.')

if __name__=='__main__':
	import sys
	main(sys.argv[1:])
	sys.exit(0)