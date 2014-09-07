from distutils.core import setup


data = {}
data['author'] = "Peleg Michaeli"
data['name'] = "DRV"
data['version'] = '0.1.1dev'
data['packages'] = ['drv', 'drv.dice']
data['license'] = open('LICENSE', 'r').read()
data['description'] = open('README.txt', 'r').read()
data['url'] = "http://github.com/pelegm/drv"
data['summary'] = "Discrete random variables in Python made easy."
data['platform'] = "Linux"


setup(**data)

