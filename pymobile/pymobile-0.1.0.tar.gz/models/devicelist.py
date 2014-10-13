import subprocess
from xml.etree.ElementTree import fromstring
import settings

# liste over PC-navn, IP, MAC og status. fyll inn flere PC-er her
devicelist = [  
    ["PC1", "127.0.0.1", "00:00:00:00:00:00"],
    ["PC2", "192.168.1.2", "00:00:00:00:00:11"],
    ["PC3", "192.168.200.200", "00:00:00:00:00:12"]
    ]

devices = list()

class Device(object):
    def __init__(self,name,ip,mac):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.start = False
        self.stop = False
        self.up = False
        self.down = False

    def update(self, up):
        if self.start and up:
            self.down = False
            self.start = False
        elif self.stop and not up:
            self.start = False
            self.stop = False
            
        self.up = up
        self.down = not up
            
    
# Legger til kolonne for status
for dev in devicelist:
    devices.append(Device(*dev))

def getDevices():
    return devices

def updateDevicesFromNmap():
    if "local_subnet" in dir(settings):
        if settings.local_subnet:
            global devices
            rawxml = subprocess.check_output(['nmap', '-sP', '-T4', '-oX', '-', settings.local_subnet], universal_newlines=True)
            root = fromstring(rawxml)
            hosts = root.findall("./host")
            for i, host in enumerate(hosts):
                
                dev = Device("","","")
                dev.name = "PC {}".format(i)
                dev.up = (host.find("status").get('state', 'down').lower() == 'up')
                dev.down != dev.up
                
                for addr in host.findall("address"):
                    if 'ipv' in addr.get('addrtype',''):
                        dev.ip = addr.get('addr','')
                    elif addr.get('addrtype','') == 'mac':
                        dev.mac = addr.get('addr','')
                        
                devices.append(dev)
