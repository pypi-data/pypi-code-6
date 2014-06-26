#############################################################################
# Author  : Jerome ODIER
#
# Email   : jerome.odier@cern.ch
#
# Version : 2.0.0 (2014)
#
#############################################################################

import sys, types, argparse

#############################################################################

def add_csp_argument(self, table_dict, table_name, no_prefix = True):

	for field, descr in sorted(table_dict.items()):

		if not field.startswith('@'):
			#####################################################
			# SPLIT FIELD DESCRIPTION                           #
			#####################################################

			descr = [x.strip() for x in descr.split('=')]

			#####################################################
			# HELP AND OPTION NAME                              #
			#####################################################

			DEFAULT = None

			HELP_PARTS = ['comma separated parameters']

			#####################################################

			if no_prefix:

				if len(descr) > 1:

					DEFAULT = descr[1]

					HELP_PARTS.append('default: `%s`' % DEFAULT)

				OPTION = '--%s' % (field.replace('_', '-'))
			else:
				OPTION = '--%s.%s' % (table_name, field.replace('_', '-'))

			#####################################################
			# ADD OPTION                                        #
			#####################################################

			try:
				self.add_argument(OPTION, help = ', '.join(HELP_PARTS), default = DEFAULT, metavar = 'XXX')

			except argparse.ArgumentError:
				pass

#############################################################################

argparse.ArgumentParser.add_csp_argument = add_csp_argument

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
