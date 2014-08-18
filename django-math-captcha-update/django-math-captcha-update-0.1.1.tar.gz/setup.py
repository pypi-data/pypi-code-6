from distutils.core import setup


setup(name='django-math-captcha-update',
      version='0.1.1',
      description='Simple, secure math captcha for django forms(Django 1.6+ compatible)',
      long_description=open('README.rst').read(),
      author='Justin Quick',
      author_email='justquick@gmail.com',
      url='http://github.com/justquick/django-math-captcha',
      packages=['math_captcha'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      )
