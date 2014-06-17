
from menu import choice

RE_HARDWARE_ADDRESS = "([\da-f]{2}:){5}[\da-f]{2}"

def pick_network_interface(func):
    import os
    import re
    import manuf
    def choice_generator():
        for interface in os.listdir("/sys/class/net"):
            if interface == "lo":
                continue

            hardware_address = open(os.path.join("/sys/class/net", interface, "address")).readline().strip().lower()
            if not re.match(RE_HARDWARE_ADDRESS, hardware_address):
                continue
                
            title = "% 9s %s" % (interface, hardware_address)
                
            if interface.startswith("vboxnet"):
                title += " VirtualBox host-only adapter"
            else:
                title += " " + manuf.get(hardware_address, "Unknown network interface controller")
                if os.path.exists(os.path.join("/sys/class/net", interface, "phy80211")):
                    title += " 802.11 wireless"
            yield title, interface
            
    def wrapped(*args):
        return func(choice(
            choice_generator(),
            "Select network interface",
            "Select network inteface you want to reconfigure"), *args)
        
    return wrapped

        

