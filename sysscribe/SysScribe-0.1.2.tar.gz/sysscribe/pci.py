from sysscribe import pciinfo

def pci_list():
    pciinf = pciinfo()
    pci_list=[]
    for pci in pciinf.keys():
        pci_list.append(pciinf[pci])
    return pci_list
        
def print_list():
    pciinf = pciinfo()
    for pci in pciinf.keys():
        print(pciinf[pci])
        
