#############################################################################
# Author  : Jerome ODIER
#
# Email   : jerome.odier@cern.ch
#
# Version : 3.0.0 (2014)
#
#############################################################################

import sys, argparse

#############################################################################

if sys.version_info[0] < 3:
	#####################################################################

	class AliasedSubParsersAction(argparse._SubParsersAction):
		#############################################################

		class AliasedAction(argparse.Action):
			#####################################################

			def __init__(self, dest, aliases, help):

				if aliases:
					dest +=  ' (%s)' % ','.join(aliases)

				super(AliasedSubParsersAction.AliasedAction, self).__init__(option_strings = [], dest = dest, help = help)

		#############################################################

		def add_parser(self, name, **kwargs):
			#####################################################
			# EXTRACT ALIAS LIST                                #
			#####################################################

			if kwargs.has_key('aliases'):
				aliases = set(kwargs['aliases'])

				del kwargs['aliases']

			else:
				aliases = set()

			#####################################################
			# CREATE SUBPARSER AND ALIASES                      #
			#####################################################

			result = super(AliasedSubParsersAction, self).add_parser(name, **kwargs)

			for alias in aliases:
				self._name_parser_map[alias] = result

			#####################################################
			# CREATE HELP                                       #
			#####################################################

			if kwargs.has_key('help'):
				help = kwargs.pop('help')
				self._choices_actions.pop()
				self._choices_actions.append(AliasedSubParsersAction.AliasedAction(name, aliases, help))

			#####################################################

			return result

	#####################################################################

	def patch(parser):
		parser.register('action', 'parsers', AliasedSubParsersAction)

else:

	def patch(parser):
		pass

#############################################################################
