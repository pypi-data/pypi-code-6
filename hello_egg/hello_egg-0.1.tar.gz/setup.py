import distutils.core

version = '0.1'

distutils.core.setup(
        name='hello_egg',
        version=version,
        packages=['hello_egg'],
        author='Justin Li',
        author_email='justinli.ljt@gmail.com',
        url='http://github.com/jizhouli',
        license='http://opensource.org/licenses/mit-license.php',
        description='say hello to the egg'
        )
