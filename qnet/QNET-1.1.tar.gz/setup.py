from distutils.core import setup
from pkgutil import walk_packages
import qnet
# from distutils.extension import Extension
#
# from Cython.Distutils import build_ext
# import numpy as np
#
#
# ext_modules = [
#     Extension("qnet.misc.kerr_cysolve",
#               ["qnet/misc/src/kerr_cysolve.pyx"],
#               include_dirs=[np.get_include()],
#               extra_link_args=['-lm']),
# ]

version = "1.1"

def find_packages(path=".", prefix=""):
    yield prefix
    prefix = prefix + "."
    for _, name, ispkg in walk_packages(path, prefix):
        if ispkg:
            yield name

packages = list(find_packages(qnet.__path__, qnet.__name__))
print packages

setup(
    name='QNET',
    version=version,
    description="""Tools for symbolically analyzing quantum feedback networks.""",
    scripts=["bin/parse_qhdl.py"],
    author="Nikolas Tezak",
    author_email="nikolas.tezak@gmail.com",
    url="http://github.com/mabuchilab/QNET",
    # cmdclass={'build_ext': build_ext},
    packages=packages,
    # ext_modules=ext_modules,
    requires=[
        'sympy',
        # 'Cython',
        'numpy',
        'qutip',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
        'Environment :: IPython notebook',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Quantum Feedback Circuits'
    ],
)
