from setuptools import setup


setup(
    name='reqs.txt',
    version='0.1',
    license='MIT',
    description='This is joke :) Be careful!',
    keywords='requirements reqs install',
    url='https://github.com/saippuakauppias/reqs.txt',
    author='Denis Veselov',
    author_email='progr.mail@gmail.com'
)


print """\x1B[31m
Be careful!
This is not \033[4mreqs.txt\033[00m\x1B[31m file!
This is a package. You missed "\x1b[7m-r\033[00m\x1B[31m" option in "\x1b[1mpip install\033[00m\x1B[31m" command.
"""
