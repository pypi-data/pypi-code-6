# -*- coding: utf-8 -*-

# Soya 3D
# Copyright (C) 2001-2014 Jean-Baptiste LAMY
# http://www.lesfleursdunormal.fr/static/informatique/soya3d/index_en.html

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, os.path, sys, glob, distutils.core, distutils.sysconfig
if ("upload_docs" in sys.argv) or ("build_sphinx" in sys.argv): import setuptools

from io import StringIO
from os.path import exists
from distutils.core import setup, Extension
from tempfile import NamedTemporaryFile

# Modify the following if needed :
HAS_SOUND = 1
HAS_TEXT  = 1
HAS_ODE   = 0
HAS_CAL3D = 1
OPENGL    = "full"
#OPENGL    = "es"

UNIVERSAL_BINARY = 1 #try to build a UB if possible

INCDIR = [
  ".",
  "/usr/include",
  "/usr/local/include",
  "/usr/X11R6/include",
  "/usr/X11/include",
  "/usr/include/freetype2",
  "/usr/X11/include/freetype2",
  "/usr/local/include/freetype2",
  "/usr/include/cal3d",
  "/usr/local/include/cal3d",
  "/sw/include", # For Mac OS X "fink"
  "/opt/local/include",# For Mac OS X "darwin port"
  "/opt/local/include/freetype2", # For Mac OS X "darwin port"
  ]
LIBDIR = [
  "/usr/lib",
  "/usr/local/lib",
  "/opt/local/lib", # For Mac OS X "darwin port"
  "/usr/X11R6/lib",
  "/usr/X11/lib",
  "/sw/lib/", # For Mac OS X "fink"
  ]
  
COMPILE_ARGS = [
  "-w",  # with GCC ; disable (Pyrex-dependant) warning
  "-fsigned-char", # On Mac, char are unsigned by default, contrary to Linux or Windows.
  ]
LINK_ARGS = []




def framework_exist(framework_name): #Os X related stuff. test if a .Framework are present or not.
  tmp = NamedTemporaryFile()
  ret = os.system("ld -framework %s -o %s -r 2> /dev/null"%(framework_name,tmp.name))
  return not ret



BUILDING   = ("build"   in sys.argv[1:]) and not ("--help" in sys.argv[1:])
INSTALLING = ("install" in sys.argv[1:]) and not ("--help" in sys.argv[1:])
SDISTING   = ("sdist"   in sys.argv[1:]) and not ("--help" in sys.argv[1:])


build_ext = None

if "--nocython" in sys.argv[1:]: sys.argv.remove("--nocython")
else:
  try:    from Cython.Distutils import build_ext
  except: pass
  
if build_ext: print("Cython found - compilation enabled")
else:         print("Cython not found - compilation disabled")

# env hack as pyrex change this variable
MACOSX_DEPLOYMENT_TARGET  = os.getenv('MACOSX_DEPLOYMENT_TARGET')
if MACOSX_DEPLOYMENT_TARGET is None: os.environ.pop('MACOSX_DEPLOYMENT_TARGET', None)
else:                                os.environ['MACOSX_DEPLOYMENT_TARGET'] = MACOSX_DEPLOYMENT_TARGET

HERE = os.path.dirname(sys.argv[0]) or "."
DEFINES = []
endian = sys.byteorder
if endian == "big": DEFINES.append(("SOYA_BIG_ENDIAN", endian))

if sys.platform[:3] == "win":
  LIBS = ["m", "glew32", "SDL2", "SDL2_image", "SDL2_mixer", "stdc++"]
  if   OPENGL == "full": LIBS.append("glew32")
else:
  LIBS = ["m", "SDL2", "SDL2_image", "stdc++"]
  FRAMEWORKS=[]
  if   OPENGL == "full": LIBS.extend(["GLEW", "GL"])
  elif OPENGL == "es"  : LIBS.extend(["GLESv1_CM", "EGL"])

SOYA_PYREX_SOURCES  = ["soya3._soya.pyx", os.path.join("c", "matrix.c"), os.path.join("c", "chunk.c")]
SOYA_C_SOURCES      = ["soya3._soya.c"  , os.path.join("c", "matrix.c"), os.path.join("c", "chunk.c")]

if HAS_SOUND:
  if "darwin" in sys.platform and framework_exist('OpenAL'):
    print("using OpenAl.Framework")
    FRAMEWORKS.append('OpenAL')
    DEFINES.append(('SOYA_MACOSX', 1))
  else:
    LIBS.append("openal")
    
if HAS_CAL3D: LIBS.append("cal3d")
if HAS_TEXT : LIBS.append("freetype")
if HAS_ODE  : LIBS.append("ode")


if BUILDING or INSTALLING:
  CONFIG_PXD_PATH = os.path.join(HERE,"config.pxd")
  CONFIG_PXD_FILE = StringIO()
  CONFIG_PXD_FILE.write("""# Machine-generated file, DO NOT EDIT!\n\n""")
  
  CONFIG_PXD_FILE.write("""DEF HAS_SOUND=%s\n"""      % HAS_SOUND)
  CONFIG_PXD_FILE.write("""DEF HAS_CAL3D=%s\n"""      % HAS_CAL3D)
  CONFIG_PXD_FILE.write("""DEF HAS_TEXT=%s\n"""       % HAS_TEXT)
  CONFIG_PXD_FILE.write("""DEF HAS_ODE=%s\n"""        % HAS_ODE)
  CONFIG_PXD_FILE.write("""DEF HAS_SHADER=1\n"""       ) # XXX 
  CONFIG_PXD_FILE.write("""DEF OPENGL="%s"\n"""       % OPENGL)
  
  if exists(CONFIG_PXD_PATH): config_pxd_orig = open(CONFIG_PXD_PATH).read()
  else:                       config_pxd_orig = ""
  if CONFIG_PXD_FILE.getvalue() != config_pxd_orig:
    print("Writing new configuration...")
    open(CONFIG_PXD_PATH, "w").write(CONFIG_PXD_FILE.getvalue())
    

  
if INSTALLING:
    auto_files = ("config.pxd",)
    missing_files = []
    for f in auto_files:
      if not os.path.exists(os.path.join(HERE,f)):
        missing_files.append(f)
    if missing_files:
      if len(missing_files)>1:
        s = ", ".join(missing_files[:-1])+" and "+missing_files[-1] + " have"
      else :
        s = missing_files[0]+ " has"
      sys.stderr.write("%s not been generated please run 'setup.py build'\n" % s)
      sys.exit(2)


if "darwin" in sys.platform:
  kernel_version = os.uname()[2] # 8.4.3
  major_version = int(kernel_version.split('.')[0])
  if UNIVERSAL_BINARY and major_version >=8 :
    os.environ['CFLAGS'] = "-arch ppc -arch i386 "+ os.environ.get('CFLAGS','')
    #try to use framework if present.
  else:
    os.environ['ARCHFLAGS'] = ' '
  to_be_remove_lib =[]
  print("Looking for available framework to use instead of a UNIX library")
  for lib in LIBS:
    if framework_exist(lib):
      to_be_remove_lib.append(lib)
      FRAMEWORKS.append(lib)
      print("%-64sfound" % ("%s.framework" % lib))
    else:
      print("%-60snot found" % ("%s.framework" % lib))
  for lib in to_be_remove_lib:
    LIBS.remove(lib)
  for framework in FRAMEWORKS:
    DEFINES.append(('HAS_FRAMEWORK_%s' % framework.upper(), 1))
    LINK_ARGS += ('-framework', framework)

# Taken from Twisted ; thanks to Christopher Armstrong :
#   make sure data files are installed in twisted package
#   this is evil.
import distutils.command.install_data
class install_data_twisted(distutils.command.install_data.install_data):
  def finalize_options(self):
    self.set_undefined_options('install', ('install_lib', 'install_dir'))
    distutils.command.install_data.install_data.finalize_options(self)



if build_ext:
  KARGS = {
    "ext_modules" : [
    Extension("soya3._soya", SOYA_PYREX_SOURCES,
              include_dirs = INCDIR, library_dirs=LIBDIR,
              libraries = LIBS, define_macros = DEFINES,
              extra_compile_args = COMPILE_ARGS,
              extra_link_args = LINK_ARGS,
              ),
    ],
    "cmdclass" : {
        'build_ext'   : build_ext,            # Pyrex magic stuff
        'install_data': install_data_twisted, # Put data with the lib
        },
    }
  
else:
  print()
  print("CYTHON NOT FOUND")
  print("Compiling the c file WITHOUT reading any .pyx files")
  print("This is OK as long as you don't modify Soya sources, and you are not building from Mercurial repository.")
  print()
  
  KARGS = {
    "ext_modules" : [
    Extension("soya3._soya", SOYA_C_SOURCES,
              include_dirs = INCDIR, library_dirs = LIBDIR,
              libraries = LIBS, define_macros = DEFINES,
              extra_compile_args = COMPILE_ARGS, 
              ),
    ],
    "cmdclass" : {
        'install_data': install_data_twisted, # Put data with the lib
        },
    }

  

setup(
  name         = "Soya3",
  version      = "0.1",
  license      = "GPL",
  description  = "A practical high-level object-oriented 3D engine for Python.",
  long_description  = """A practical high-level object-oriented 3D engine for Python 3.
Soya is designed with game in mind. It includes terrains, particles systems, animation support, shaders,...""",
  keywords     = "3D engine openGL python shader",
  author       = "Jiba (LAMY Jean-Baptiste)",
  author_email = "<jibalamy *@* free *.* fr>",
  url          = "http://www.lesfleursdunormal.fr/static/informatique/soya3d/index_en.html",
  classifiers  = [
  "Topic :: Games/Entertainment",
  "Topic :: Multimedia :: Graphics :: 3D Rendering",
  "Topic :: Software Development :: Libraries :: Python Modules",
  "Programming Language :: Python :: 3",
  "Programming Language :: Cython",
  "Intended Audience :: Developers",
  "Development Status :: 4 - Beta",
#  "Development Status :: 5 - Production/Stable",
  "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
  ],
  
  scripts      = [],
  package_dir  = {"soya3" : ""},
  packages     = ["soya3", "soya3.gui", "soya3.converter"],
  package_data = {"soya3" : ["data/*", "data/mini_shaders/*"]},
  
  #data_files   = [(os.path.join("soya3", "data"),
  #                [os.path.join("data", file) for file in os.listdir("data") if (file != "CVS") and (file != ".arch-ids") and (file != ".svn")]
  #                 )],
  **KARGS)

