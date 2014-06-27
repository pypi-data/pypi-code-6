# -*- coding: utf-8 -*-
from __future__ import (division, print_function, unicode_literals)
#############################################################################
# Author  : Jerome ODIER, Jerome FULACHIER, Fabian LAMBERT, Solveig ALBRAND
#
# Email   : jerome.odier@lpsc.in2p3.fr
#           jerome.fulachier@lpsc.in2p3.fr
#           fabian.lambert@lpsc.in2p3.fr
#           solveig.albrand@lpsc.in2p3.fr
#
# Version : 1.X.X (2014)
#
#############################################################################

def _is_not_reserved(field):

	field = field.lstrip('.')

	return field != 'PROCESS'       \
	       and                      \
	       field != 'PROJECT'       \
	       and                      \
	       field != 'AMIELEMENTID'  \
	       and                      \
	       field != 'AMIENTITYNAME'

#############################################################################

def dict_to_csv(D):
	result = ''

	fields, values = tuple(zip(*[(field, value.replace('\n', '\\n')) for field, value in list(D.items()) if _is_not_reserved(field)]))

	result += '#AMI RESULT\n'
	result += '\n'
	result += '#FIELDS\n'
	result += '%s\n' % ';'.join(fields)
	result += '#VALUES\n'
	result += '%s\n' % ';'.join(values)

	return result

#############################################################################
