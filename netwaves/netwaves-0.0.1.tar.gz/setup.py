from distutils.core import setup

setup(name='netwaves',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Record microphone to wav and netbpm.',
      url='https://github.com/tlevine/netwaves',
      install_requires = [
#         'alsaaudio',
      ],
      scripts = [
          'netwaves.py',
      ],
      tests_require = ['nose'],
      version='0.0.1',
      license='AGPL',
      classifiers=[
          'Programming Language :: Python :: 3.4',
      ],
)
