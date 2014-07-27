from distutils.core import setup

with open('LaZy_NT/_version.py') as f:
    exec(f.read())
    
setup(
    name='LaZy_NT',
    version=__version__,
    author='Marc Herndon',
    author_email='mth309@poly.edu',
    packages=['LaZy_NT'],
    url='none',
    license='LICENSE.txt',
    description='File carving for compressed NTFS volumes.',
    long_description=open('README.txt').read(),
#    extras_require = {
#        'pdf metadata' : ["pyPdf >= 1.13"],
#        'image metadata' : ["Pillow >= 2.4.0"],
#        'office metadata' : ["openxmllib >= 1.0.7"],
#        'various metadata' : ["hachoir-core >= 1.3.3",
#                              "hachoir-metadata >= 1.3.3",
#                              "hachoir-parser >= 1.3.4"]
#        }
    install_requires = [
        "pyPdf >= 1.13",
        "Pillow >= 2.4.0",
        "openxmllib >= 1.0.7",
        "hachoir-core >= 1.3.3",
        "hachoir-metadata >= 1.3.3",
        "hachoir-parser >= 1.3.4"
    ]
)
