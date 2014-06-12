
from sysscribe import meminfo

def total():
    meminf = meminfo()
    return meminf['MemTotal']

def print_total():
    print('Total memory: {0}'.format(total()))
