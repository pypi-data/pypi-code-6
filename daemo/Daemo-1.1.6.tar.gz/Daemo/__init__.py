#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple module for writting daemons.

Includes class for creating simple daemons.
"""

import os, time, signal, sys

class DaemonError(Exception):
	pass

def pass_(*args):
	pass

class Daemon(object):
	"""Basic class for creating daemons"""
	
	def __init__(self, pidfile_path, stdin=sys.stdin,
		stderr=sys.stderr, stdout=sys.stdout):
		
		if not os.path.exists(os.path.dirname(pidfile_path)):
			raise DaemonError(
				"Unable to create PID file: directory doesn't exist")
		
		self.pidfile_path = pidfile_path
		self.stdin = stdin
		self.stderr = stderr
		self.stdout = stdout
	
	def onStart(self):
		"""This method is being called when daemon starts"""
		
		pass
	
	def onStop(self):
		"""This method is being called when daemon stops"""
		
		pass
	
	def delete_pidfile(self):
		try:
			os.remove(self.pidfile_path)
		except OSError:
			pass
	
	def start(self):
		"""Start daemon"""
		
		if os.path.exists(self.pidfile_path):
			raise DaemonError("Daemon is already running")
		
		try:
			pid = os.fork()
		except OSError:
			raise DaemonError("1st fork failed")
		
		if pid != 0:
			sys.exit(0)
		
		os.setsid()
		os.umask(0)
		
		try:
			pid = os.fork()
		except OSError:
			raise DaemonError("2nd fork failed")
		
		if pid != 0:
			self.pid = pid
			sys.exit(0)
		
		sys.stdout.flush()
		sys.stderr.flush()
		
		os.dup2(self.stdin.fileno(), sys.stdin.fileno())
		os.dup2(self.stderr.fileno(), sys.stderr.fileno())
		os.dup2(self.stdout.fileno(), sys.stdout.fileno())
		
		try:
			f = open(self.pidfile_path, "w")
		except IOError:
			raise DaemonError("Unable to create/open PID file")
		
		f.write(str(os.getpid()))
		f.close()
		
		def atexit_func(signum=None, frame=None):
			self.delete_pidfile()
			sys.exit(0)
		
		signal.signal(signal.SIGTERM, atexit_func)
		signal.signal(signal.SIGINT, atexit_func)
		
		self.onStart()

	def stop(self):
		"""Stop daemon"""
				
		try:
			pid = self.pid
		except AttributeError:
			try:
				f = open(self.pidfile_path)
				pid = f.read().strip()
				f.close()
			except IOError:
				raise DaemonError("Daemon is not running")
		
		self.onStop()
		
		try:
			while True:
				os.kill(int(pid), signal.SIGTERM)
		except OSError as e:
			if str(e).find("No such process") < 1:
				raise DaemonError("Daemon is not running")
