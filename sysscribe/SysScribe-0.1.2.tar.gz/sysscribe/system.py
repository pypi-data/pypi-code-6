
from collections import OrderedDict
import platform

from sysscribe import cpu
from sysscribe import memory
from sysscribe import network
from sysscribe import disk
from sysscribe import pci
from sysscribe import product



def system_dict():
    
    sysinfo=OrderedDict()
    
    # Hardware product
    sysinfo['product'] = product()

    # OS platform
    sysinfo['platform'] = platform.uname()

    # Add cpu info dict
    cpu_list = cpu.dev_list()
    sysinfo['cpu'] = OrderedDict()
    sysinfo['cpu']['num cores'] = len(cpu_list)
    sysinfo['cpu']['socket type'] = cpu_list[0]
    sysinfo['cpu']['cores per socket'] = cpu.get_cores_per_socket()
    
    # Add memory info
    sysinfo['memory'] = OrderedDict()
    sysinfo['memory']['total'] = memory.total()
    
    # Add network info
    net_list = network.dev_list()
    sysinfo['network'] = OrderedDict()
    sysinfo['network']['num devices'] = len(net_list)
    sysinfo['network']['devices'] = net_list
    
    # Storage info
    disk_sizes = disk.disk_sizes()
    sysinfo['disk'] = OrderedDict()
    sysinfo['disk']['num devices'] = len(disk_sizes)
    sysinfo['disk']['device size'] = disk_sizes
    
    # Pci info
    pci_list = pci.pci_list()
    sysinfo['pci'] = OrderedDict()
    sysinfo['pci']['num devices'] = len(pci_list)
    sysinfo['pci']['device size'] = pci_list
    
    
    
    return sysinfo
    
    