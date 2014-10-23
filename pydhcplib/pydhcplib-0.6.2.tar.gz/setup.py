#!/usr/bin/env python2.5

from distutils.core import setup

fr8_manpages=['man/fr/man8/pydhcp.8.gz']
fr3_manpages=['man/fr/man3/pydhcplib.3.gz',
              'man/fr/man3/pydhcplib.DhcpBasicPacket.3.gz',
              'man/fr/man3/pydhcplib.DhcpPacket.3.gz',
              'man/fr/man3/pydhcplib.hwmac.3.gz',
              'man/fr/man3/pydhcplib.ipv4.3.gz',
              'man/fr/man3/pydhcplib.strlist.3.gz']
en3_manpages=['man/man3/pydhcplib.strlist.3.gz',
              'man/man3/pydhcplib.3.gz',
              'man/man3/pydhcplib.ipv4.3.gz']
en8_manpages=['man/man8/pydhcp.8.gz']

setup(name='pydhcplib',
      version="0.6.2",
      license='GPL v3',
      description='Dhcp client/server library',
      author='Mathieu Ignacio',
      author_email='mignacio@april.org',
      url='http://pydhcplib.tuxfamily.org/',
      packages=['pydhcplib'],
      scripts=['scripts/pydhcp'],
      data_files=[("share/man/man8",en8_manpages),
      #            ("share/man/fr/man8",fr8_manpages),
                  ("share/man/fr/man3",fr3_manpages),
                  ("share/man/man3",en3_manpages)
                  ])
