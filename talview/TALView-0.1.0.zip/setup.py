from distutils.core import setup
from talview import __version__
setup(
    name='TALView',
    version=__version__,
    author='Jan Brohl',
    author_email='janbrohl@t-online.de.org',
    url='https://bitbucket.org/janbrohl/talview',
    license='3-clause BSD',
    description="TAL-Templates as Views",
    py_modules=['talview'],
    requires=["simpletal (>=5.1)"],
)
