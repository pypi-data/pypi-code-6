#!h:\Python\Python34\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'mydupfilekiller==1.9','console_scripts','mydupfilekiller'
__requires__ = 'mydupfilekiller==1.9'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('mydupfilekiller==1.9', 'console_scripts', 'mydupfilekiller')()
    )
