from optparse import OptionParser
import os

class ArgumentParser:
	"""Commandline arguments"""

	options = ""
	args = ""

	def parse(self):
		self.parser = OptionParser()

		home = os.path.expanduser('~')

		self.parser.add_option("-p", "--path", dest="path", metavar="path", default=home+"/.pgpass",
                  help="Path to .pgpass. Default will be ~/.pgpass")

		self.parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                  help="print out messages")

		(self.options, self.args) = self.parser.parse_args()

	def isValid(self):
		return True

	def getPath(self):
		return self.options.path

	def isVerbose(self):
		return self.options.verbose

	def printUsage(self):
		self.parser.print_help()