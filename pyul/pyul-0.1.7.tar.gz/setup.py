import sys, setuptools

kw = {}
if sys.version_info >= (3,):
    kw['use_2to3'] = True

setuptools.setup(
    setup_requires=['pbr==0.9.0.5.gafbf133'],
    pbr=True,
    **kw)
