from setuptools import setup

setup(
    name='bitcoinWebRPC',
    version='0.1',
    description='Bitcoin WebRPC for Python',
    long_description='Bitcoin RPC calls via HTTP and Web using flask underneath' ,
    url='https://github.com/benjyz/bitcoinWebRPC',
    author='Flying Circus',
    license='MIT',
    packages=['bitcoinwebrpc'],
    zip_safe=False
)

"""
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Topic :: Office/Business :: Financial'
    ],
    packages=find_packages("src"),
    package_dir={'': 'src'}
)
"""
