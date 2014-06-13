from sysscribe import cpuinfo

def dev_list():
    cpuinf = cpuinfo()
    cpu_list=[]
    for processor in cpuinf.keys():
        cpu_list.append(cpuinf[processor]['model name'])
    return cpu_list
        
def print_list():
    cpuinf = cpuinfo()
    for processor in cpuinf.keys():
        print(cpuinf[processor]['model name'])
        
def get_cores_per_socket():
    cpuinf = cpuinfo()
    for processor in cpuinf.keys():
        return cpuinf[processor]['cpu cores']
    
    return 0