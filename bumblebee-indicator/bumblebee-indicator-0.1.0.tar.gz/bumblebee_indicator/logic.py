import logging
import re
import os.path as p

class Optimus:
	
	class DualMonitor:
		def __init__(self, optimus):
			pass
		def is_active(self):
			# grep -q 'PMMethod=none' /etc/bumblebee/bumblebee.conf
			proc_file = file(p.join('/', 'etc', 'bumblebee', 'bumblebee.conf'))
			contents = proc_file.read().strip()
			logging.debug('DualMonitor::is_active() - /etc/bumblebee/bumblebee.conf: %s' % contents[-100:-1])
			regex = re.compile('^PMMethod=none\s*?(?:\#.*)?$', re.MULTILINE)
			match = regex.search(contents)
			ret = match != None
			logging.debug('DualMonitor::is_active() %s' % repr(ret))
			return ret
		def turn(self, setting = True):
			pass
	
	def __init__(self):
		self.__dual = Optimus.DualMonitor(self)
		
	def is_active(self):
		# cat /proc/acpi/bbswitch
		proc_file = file(p.join('/', 'proc', 'acpi', 'bbswitch'))
		contents = proc_file.read().strip()
		logging.debug('Optimus::is_active() - /proc/acpi/bbswitch: %s' % repr(contents))
		idx = contents.rfind('ON')
		ret = idx >= 0
		logging.debug('Optimus::is_active() => %s' % repr(ret))
		return ret
	
	def dual_monitor(self):
		return self.__dual
	
	
