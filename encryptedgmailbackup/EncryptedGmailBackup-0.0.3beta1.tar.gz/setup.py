#!/usr/bin/env python

from setuptools import setup

setup(name='EncryptedGmailBackup',
      version='0.0.3beta1',
      description='Backup your GMail account with GPG encryption.',
      author='Stephen Holiday',
      author_email='stephen.holiday@gmail.com',
      url='https://github.com/sholiday/encrypted-gmail-backup',
      py_modules=['gmailbackup'],
      scripts=['dobackup.py'],
      entry_points={
          'console_scripts': [
              'gmail-backup = dobackup:main',
          ]
      },
      include_package_data = True,
      package_data={
    	'': ['defaults.ini'],
	  },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python',
      ],
      install_requires=['gnupg', 'psutil'],
      long_description="""

   Place your config in in `~/.encrypted_gmail_backup`

   Sample Config:

	[gmail]
	username = stephen.holiday@gmail.com
	password = changeme

	[gpg]
	keyid = 76AA7B2CF3FD360E
	binary = gpg

	[backup]
	path = /backup/gmail/
	metafile = gmailmeta.txt
	archive = messages.tar

  Be sure to `chmod 600 ~/.encrypted_gmail_backup` so that other users can't read your password.

  I have MacGPG installed on my system, so I changed binary to:

	binary = /usr/local/MacGPG2/bin/gpg2

  The full configuration can be seen in `defaults.ini`.
   """, requires=['gnupg', 'psutil']
)
