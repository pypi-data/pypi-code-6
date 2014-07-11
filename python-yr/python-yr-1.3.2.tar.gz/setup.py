#!/usr/bin/env python3

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

#try:
#    from pypandoc import convert
#    read_md = lambda filename: convert(filename, 'rst')
#except ImportError:
#    print("warning: pypandoc module not found, could not convert Markdown to RST")
#    read_md = lambda filename: open(filename, mode='r').read()
#long_description = read_md('README.md')

#import pandoc
#pandoc.PANDOC_PATH = '/usr/bin/pandoc'
#doc = pandoc.Document()
#doc.markdown = open('README.md', mode='r').read()
#long_description = doc.rst

#long_description = open('README.md', mode='r').read()

long_description = '''\
python-yr
=================
Library for the norwegian wheather service yr.no in python.

#### Usage
```python
from yr.libyr import Yr

weather = Yr(location_name='Norge/Telemark/Skien/Skien')
now = weather.now(as_json=True)

print(now)
```

#### This returns
```json
{
    "@from": "2014-06-04T08:00:00", 
    "@to": "2014-06-04T12:00:00", 
    "@period": "1", 
    "symbol": {
        "@number": "3", 
        "@numberEx": "3", 
        "@name": "Partly cloudy", 
        "@var": "03d"
    }, 
    "precipitation": {
        "@value": "0", 
        "@minvalue": "0", 
        "@maxvalue": "0.1"
    }, 
    "windDirection": {
        "@deg": "159.4", 
        "@code": "SSE", 
        "@name": "South-southeast"
    }, 
    "windSpeed": {
        "@mps": "1.3", 
        "@name": "Light air"
    }, 
    "temperature": {
        "@unit": "celsius", 
        "@value": "13"
    }, 
    "pressure": {
        "@unit": "hPa", 
        "@value": "1012.1"
    }
}
```

For more usage examples visit folder [examples](/yr/examples) or project [wiki](https://github.com/wckd/python-yr/wiki)

Pull requests are very welcomed! :-)

#### Changelog

1.3.2 (2014 Jul 11)

* Improved exception-handling, thanks @mbambas!

1.3.1.1 (2014 Jul 10)

* Bugfix: pypi/pip installer in 'setup.py'

1.3.1 (2014 Jul 10)

* Bugfix: caching mechanism in 'is_fresh' function ~> thanks to antorweep
* Improve examples
'''

setup(
    name = 'python-yr',
    version = '1.3.2',
    description = 'Get the forecast from the norwegian wheather service yr.no in python',
    long_description = long_description,
    author = 'Alexander Hansen',
    author_email = 'alexander.l.hansen@gmail.com',
    maintainer = 'GNU Knight',
    maintainer_email = 'idxxx23@gmail.com',
    url = 'https://github.com/wckd/python-yr',
    packages = ['yr'],
    package_data = {
        'yr': [
            'examples/*.py',
            'languages/*.json',
            'locations/*.gz',
            'README.md',
        ]
    },
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet',
    ],
    install_requires = ['xmltodict'], # $$solve$$ ~> /usr/lib/python3.4/distutils/dist.py:260: UserWarning: Unknown distribution option: 'install_requires' warnings.warn(msg)
)
