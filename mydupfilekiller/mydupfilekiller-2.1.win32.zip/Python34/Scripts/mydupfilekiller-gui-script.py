#!h:\Python\Python34\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'mydupfilekiller==2.1','console_scripts','mydupfilekiller-gui'
__requires__ = 'mydupfilekiller==2.1'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('mydupfilekiller==2.1', 'console_scripts', 'mydupfilekiller-gui')()
    )
