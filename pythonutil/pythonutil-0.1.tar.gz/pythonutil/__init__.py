from OpenStackUtil import Keystone, URL
from JSONUtil import LoadJSON, pretty_print
from FileUtil import File


if __name__ == '__main__':
     Keystone.set_config(keystone_ip="192.168.0.106", username="demo",password="nova")
     '''see which class or methods has been imported'''
     print dir()