import platform
import os
from collections import OrderedDict
import pprint

VERSION = (0, 1, 1)
__version__ = '.'.join(map(str, VERSION)) + '-dev'


def cpuinfo():
    ''' Return the information in /proc/cpuinfo
    as a dictionary in the following format:
    cpu_info['proc0']={...}
    cpu_info['proc1']={...}

    '''

    cpuinfo=OrderedDict()
    procinfo=OrderedDict()

    nprocs = 0
    with open('/proc/cpuinfo') as f:
        for line in f:
            if not line.strip():
                # end of one processor
                cpuinfo['proc%s' % nprocs] = procinfo
                nprocs=nprocs+1
                # Reset
                procinfo=OrderedDict()
            else:
                if len(line.split(':')) == 2:
                    procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                else:
                    procinfo[line.split(':')[0].strip()] = ''
            
    return cpuinfo


def pciinfo():
    pciinfo=OrderedDict()
    with os.popen('/sbin/lspci') as f:
        for line in f:
            pciinfo[line.split(' ')[0]] = line.split(' ',1)[1].strip()
    return pciinfo

def meminfo():
    ''' Return the information in /proc/meminfo
    as a dictionary '''
    meminfo=OrderedDict()

    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo

from collections import namedtuple

def netdevs():
    ''' RX and TX bytes for each of the network devices '''

    with open('/proc/net/dev') as f:
        net_dump = f.readlines()
    
    device_data={}
    data = namedtuple('data',['rx','tx'])
    for line in net_dump[2:]:
        line = line.split(':')
        if line[0].strip() != 'lo':
            device_data[line[0].strip()] = data(float(line[1].split()[0])/(1024.0*1024.0), 
                                                float(line[1].split()[8])/(1024.0*1024.0))
    
    return device_data

import glob
import re
import os

# Add any other device pattern to read from
dev_pattern = ['sd.*','mmcblk*']

def size(device):
    nr_sectors = open(device+'/size').read().rstrip('\n')
    try:
        sect_size = open(device+'/queue/hw_sector_size').read().rstrip('\n')
    except: # For rh5.4 need the following
        sect_size = open(device+'/queue/max_sectors_kb').read().rstrip('\n')

    # The sect_size is in bytes, so we convert it to GiB and then send it back
    return (float(nr_sectors)*float(sect_size))/(1024.0*1024.0*1024.0)

def detect_devs():
    for device in glob.glob('/sys/block/*'):
        for pattern in dev_pattern:
            if re.compile(pattern).match(os.path.basename(device)):
                print('Device:: {0}, Size:: {1} GiB'.format(device, size(device)))
                
def detect_dev_sizes():
    dev_size=[]
    for device in glob.glob('/sys/block/*'):
        for pattern in dev_pattern:
            if re.compile(pattern).match(os.path.basename(device)):
                dev_size.append(size(device))
    return dev_size


def product():
    vendor_str="unknown"
    try:
        with open('/sys/devices/virtual/dmi/id/product_name') as f:
            vendor_str = f.readline()
    except:
        pass
    return vendor_str        
    

def echo():
    from sysscribe import system
    print system.system_dict()
