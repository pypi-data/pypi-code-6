#!/usr/bin/env python

""" Distutils Setup File for the eGenix web installer test package.

"""
#
# Run web installer, if needed
#
import mxSetup, os
#mxSetup._debug = 3
mxSetup.run_web_installer(
    os.path.dirname(os.path.abspath(__file__)),
    landmarks=('mx', 'PREBUILT'))

# Debug output
if 0:
    import os, sys
    print ('command line: %s %s' % (sys.executable, ' '.join(sys.argv)))
    print ('work dir: %r' % os.listdir('.'))

#
# Load configuration(s)
#
import egenix_web_installer_test
configurations = (egenix_web_installer_test,)

#
# Run distutils setup...
#
import mxSetup
mxSetup.run_setup(configurations)
