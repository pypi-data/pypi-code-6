
import netifaces


for iface in netifaces.interfaces():
    try:
        ip = netifaces.ifaddresses(iface)[2][0]['addr']
        print "{} : {}".format(iface, ip)
    except:
        pass

