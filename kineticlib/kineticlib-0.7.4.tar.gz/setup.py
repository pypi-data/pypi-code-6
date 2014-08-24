from distutils.core import setup

setup(name='kineticlib',
      version='0.7.4',
      description='Library for kinetic theory calculations in the multi-temperature and state-to-state approximations',
      author='George Oblapenko',
      author_email='kunstmord@kunstmord.com',
      url='https://github.com/Kunstmord/kineticlib',
      license="GPL",
      packages=['kineticlib'],
      package_dir={'kineticlib': 'src/kineticlib'},
      package_data={'kineticlib': ['data/models/*.csv', 'data/particles/*.dat', 'data/spectra/*.dat']},
      requires=['numpy', 'scipy'],
      include_package_data=True,
      classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
        ],
      long_description = """\
      KineticLib
      ==========

      Provides a library with various functions used in computational kinetic theory.
      Aimed at the multi-temperature (and one-temperature as a special case) and state-to-state approximations.

      Documentation is available here: http://kineticlib.readthedocs.org/en/latest/

      For changes see CHANGELOG.txt (https://github.com/Kunstmord/kineticlib/blob/master/CHANGELOG.txt)


      Roadmap (major additions)
      =========================

      * Add calculation of heat capacities for mixtures and partial derivatives of full internal energy with respect to
        numeric density

      * Add pre-made calculations of simple things (like shear viscosity)

      * More vibrational models - Landau-Teller, SSH

      Current issues
      ==============

      #. VV probabilities seem to be wrong for multi-quantum transitions. Needs more thorough literature checks

      #. Rotational relaxation times calculated using a strict definition seem to be off by a factor of 2.
      """
      )