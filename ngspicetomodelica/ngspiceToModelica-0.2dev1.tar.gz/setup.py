try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

desc = """\
More details on the project
===========================
This project converts an ngspice netlist to Modelica code. It can handle device models for diode and MOSFETs, and subcircuits. Currently BJTs, JFETs are not supported. Xspice is also not currently supported.
"""

setup(
    name='ngspiceToModelica',
    version='0.2dev1',
    description='A python project to convert ngspice netlists to Modelica code',
    long_description=desc,
    url='https://pypi.python.org/pypi/ngspiceToModelica',
    author='Rakhi R',
    author_email='rakhiwarriar@iitb.ac.in',
    license='GPL',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
	'Intended Audience :: End Users/Desktop',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='ngspice to modelica code conversion',
    py_modules = ['NgspicetoModelica']
)
