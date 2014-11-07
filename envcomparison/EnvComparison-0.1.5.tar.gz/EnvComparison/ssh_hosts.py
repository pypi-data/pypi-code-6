from paramiko import SSHConfig

def get_host_list(config_location):
    config = SSHConfig()
    config.parse(open(config_location))
    host_list = [new['host'][0] for new in config.__dict__['_config'][1:]]
    i = 0
    host_menu = {}
    for host in host_list:
        host_menu[i] = host
        i+=1
    return host_menu


