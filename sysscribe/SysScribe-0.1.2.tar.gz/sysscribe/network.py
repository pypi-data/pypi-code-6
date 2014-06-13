
from sysscribe import netdevs

def dev_list():
    netdev = netdevs()
    net_list=[]
    for dev in netdev.keys():
        net_list.append(dev)
    return net_list

def print_rxtx():
    netdev = netdevs()
    for dev in netdev.keys():
        print('{0}: {1} MiB {2} MiB'.format(dev, netdev[dev].rx, netdev[dev].tx))
