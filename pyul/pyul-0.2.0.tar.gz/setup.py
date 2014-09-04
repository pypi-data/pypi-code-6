import sys, setuptools

kw = {}
if sys.version_info >= (3,):
    kw['use_2to3'] = True

setuptools.setup(
    setup_requires=['pbr==0.11.0.dev19.gb0cedad'],
    pbr=True,
    **kw)
