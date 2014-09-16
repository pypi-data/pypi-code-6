__author__ = 'Tanner Baldus'
"""
File for storing makefile templates. To use in settings simply add the line:
from makefile_templates import template_name
to settings.py
"""

gnumake_template = """
# TESTRUNNER:       the path to the testrunner
# LIST_SUITES:      how to list available test suites.
# RUN_ONE_SUITE:    how to run a single suite, should use the special
#           variable $1 which will be replaced by the suite name.

TESTRUNNER    = ./{testrunner}
LIST_SUITES   = {list_cmd}
RUN_ONE_SUITE = $(TESTRUNNER) {run_cmd}

###############################################################################
# DO NOT MODIFY BELOW THIS LINE

include suites.def
TARGETS=$(addsuffix _test,$(SUITES))

all: $(TARGETS)

%_test:
	$(call RUN_ONE_SUITE,$*)

suites.def: $(TESTRUNNER)
	echo "SUITES=" > $@
	for n in `$(LIST_SUITES)` ; do echo "SUITES += $$n" >> $@ ; done
"""


