try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

from Cython.Distutils import build_ext
import pkg_resources

# data_dir = pkg_resources.resource_filename("autowrap", "data_files")

ext = Extension("tree_distance",
                language='c++',
                sources = ['cpp/BipartiteGraph.cpp',
                           'cpp/Bipartition.cpp',
                           'cpp/Distance.cpp',
                           'cpp/EdgeAttribute.cpp',
                           'cpp/Geodesic.cpp',
                           'cpp/PhyloTree.cpp',
                           'cpp/PhyloTreeEdge.cpp',
                           'cpp/Ratio.cpp',
                           'cpp/RatioSequence.cpp',
                           'cpp/Tools.cpp',
                           'cpp/cython/TreeDistance.pyx'],
                # include_dirs = [data_dir],
                extra_compile_args=['-std=c++11'],
               )

setup(cmdclass={'build_ext':build_ext},
      name="tree_distance",
      version="0.0.1",
      author='Kevin Gori',
      author_email='kgori@ebi.ac.uk',
      description='Wrapper for GTP tree distances in c++',
      url='https://github.com/kgori/GTP.git',
      ext_modules = [ext],
      install_requires=[
        'cython',
      ],
     )
