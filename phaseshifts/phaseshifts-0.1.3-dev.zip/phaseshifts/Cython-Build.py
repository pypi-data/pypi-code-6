from numpy.distutils.core import setup
# from distutils.core import setup
from numpy.distutils.extension import Extension

import os, sys

# we'd better have Cython installed, or it's a no-go
try:
    from Cython.Distutils import build_ext
    from Cython.Build import cythonize
except:
    sys.stderr.write("You don't seem to have Cython installed. Please get a "
          "copy from www.cython.org and install it\n")
    sys.exit(1)

# build Cython extensions
for module in ['atorb.pyx', 'conphas.pyx', 'elements.pyx', 'leed.pyx', 'model.pyx']:
    setup(
      cmdclass={'build_ext': build_ext},
      ext_modules=cythonize([module]),
    )

# build f2py extensions
from numpy.distutils.core import setup as f2py_setup
f2py_setup(
    ext_modules=[Extension(name='libphsh',
                  sources=[os.path.join('lib','libphsh.f')])],
)

# try:
    # import py2exe 
    # sys.argv.append('py2exe')
    
    # setup(
        # name = 'phaseshifts',
        # zipfile = None,
        # options={
            # 'py2exe': {
                # 'bundle_files': 1, 
                # 'compressed': True,
                # 'packages': ['numpy'],
                # 'dist_dir': os.path.join("dist", "py2exe"),
                # 'dll_excludes':['w9xpopen.exe', 'tk85.dll', 'tcl85.dll'],  # Exclude standard library dlls
                # 'excludes': ['_ssl', 'pyreadline', 'difflib', 'doctest', 'locale',
                            # 'optparse', 'pickle', 'calendar', 'pbd', 'unittest', 
                            # 'inspect', 'tk', 'numpy', 'xml'],  # Exclude standard library
                # 'includes': ['numpy',],
            # }
        # },
        # console=[
            # {'script': 'phsh.py',
            # 'icon_resources': [(0, 'phaseshifts.ico')],
            # }
        # ],
        
    # )
# except ImportError:
    # sys.stderr.write("You don't seem to have py2exe installed. Please get a "
          # "copy from www.py2exe.org and install it\n")
    # sys.exit(1)
          
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

setup(  name = "phaseshifts",
        version = "0.1",
        description = "Generate atomic phase shifts",
        options = {"build_exe": build_exe_options},
        executables = [Executable("phsh.py", base=None)]
    )
          