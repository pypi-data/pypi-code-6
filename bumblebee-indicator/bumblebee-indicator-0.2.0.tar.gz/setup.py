#!/usr/bin/env python2

from setuptools import setup
from distutils.command.install_data import install_data

cmdclasses = {'install_data': install_data}
data_files = [
	('/etc/xdg/autostart', ['etc/xdg/autostart/bumblebee-indicator.desktop']),
	('/usr/share/applications', ['etc/xdg/autostart/bumblebee-indicator.desktop']),
	('/usr/share/pixmaps', ['bumblebee_indicator/resources/bumblebee-icon-active.png']),
	('/usr/local/bin/hidden', ['usr/local/bin/hidden/nvidia-enable', 'usr/local/bin/hidden/nvidia-disable']),
	('/usr/lib/bumblebee-indicator', ['usr/lib/bumblebee-indicator/enable.aug', 'usr/lib/bumblebee-indicator/disable.aug'])
]

setup(
  name         = 'bumblebee-indicator',
  version      = '0.2.0',
  description  = 'A Unity desktop bumblebee indicator - switch dual screen on/off, enable 3d mode',
  url          = 'http://github.com/wavesoftware/bumblebee-indicator',
  author       = 'Wave Software',
  author_email = 'info@wavesoftware.pl',
  license      = 'Apache License 2.0',
  packages     = ['bumblebee_indicator'],
  zip_safe     = True,
  scripts      = ['bin/bumblebee-indicator'],
  cmdclass     = cmdclasses,
  data_files   = data_files, 
  package_data = { 
    '': ['resources/*']
  }
)
