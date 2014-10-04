from pysite.exceptions.conf import *
import imp
from os.path import abspath,dirname,join,normpath

class PySiteConfiguration(object):
	def __init__(self,basedir,sitename=None,sitetitle=None,logfile=None):
		self.basedir = basedir
		self.basedir_a = abspath(normpath(basedir))
		if sitename:
			self.sitename = sitename
			
		if not getattr(self,'sitename',None):
			raise ConfException('Mandatory configuration member "sitename" is missing')
		
		if sitetitle:
			self.sitetitle = sitetitle
		elif not getattr(self,'sitetitle',None):
			self.sitetitle = self.sitename

		if logfile:
			self.logfile = logfile
		elif not getattr(self,'logfile',None):
			self.logfile = join(self.basedir,'%s.log' % self.sitename)

	def basedir_abspath(self):
		"""
		Get the absolute path to the site base directory
		
		@rtype: string
		"""
		return self.basedir_a

global_conf = None

def getConfiguration(basedir=None):
	global global_conf
	if not global_conf:
		confmod = imp.load_source('conf',join(basedir,'conf.py'))
		global_conf = confmod.siteconf(basedir)
	return global_conf

get_conf = getConfiguration