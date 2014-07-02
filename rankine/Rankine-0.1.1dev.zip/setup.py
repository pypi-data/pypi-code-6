from distutils.core import setup


setup(
    name='Rankine',
    version='0.1.1dev',
    description="Python tools for working with Valve's Steamworks Web API (https://partner.steamgames.com/documentation/webapi).",
    #long_description=open('README.rst').read(),
    classifiers=[
        #'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        #'Topic :: Scientific/Engineering',
    ],
    #keywords='HCUP SAS healthcare analysis pandas',
    author='T.J. Biel',
    author_email='terry.biel@gmail.com',
    packages=['rankine'],
    license='MIT',
    provides=['rankine'],
    #requires=['pandas (>=0.11.0)'],
    #package_data={'pyhcup': [
    #                'data/loadfiles/*/*.*',
    #                'data/uflags/*.*',
    #                'data/maps/*.*',
    #                ]
    #                },
)