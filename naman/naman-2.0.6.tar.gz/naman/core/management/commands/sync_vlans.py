# -*- coding: utf-8 -*-
from naman.core.models import *
from django.db import connections, DatabaseError
import ipaddr
from django.core.management.base import BaseCommand, CommandError
redip = connections['redip'].cursor()
#bahamas = connections['bahamas'].cursor()


class Command(BaseCommand):
    args = ''
    help = """

"""

    vlan_map = {}

    def sync_dbred_vlans(self, path):

        fo = open(path, "r")
        for vlan in fo.readlines():
            vlan = vlan.replace("\r\n", "")
            fields = vlan.split(",")
            if len(fields) != 4:
                continue

            print(fields)

            if fields[1] in ("L2", "*"):
                net_ip = "0.0.0.0"
                mask = 0
            else:
                net_ip = fields[1]
                mask = fields[2]

            red = ipaddr.IPv4Network("%s/%s" % (net_ip, mask))
            gw = "0.0.0.0"
            for host in red.iterhosts():
                gw = host
                break

            VLan.objects.get_or_create(
                name=fields[0],
                ip=net_ip,
                mask=mask,
                tag=fields[3],
                gw=gw
            )


    def mapea_vlan(self, arqred_name, path):
        if len(self.vlan_map) == 0:
            self.load_mapeo_vlans()

        if arqred_name in self.vlan_map.keys():
            return self.vlan_map[arqred_name]
        return arqred_name


    def load_mapeo_vlans(self, path):

        f = open(path, "r")

        for line in f.readlines():
            values = line.split(",")
            self.vlan_map[values[0]] = values[1]








    def handle(self, *args, **options):

        self.read_dbred_vlans(args[0])
        return

        print args

        """"
        args[0] tiene que pasar el path al fichero de vlans exportado desde bdred con el template de exportacion
        args[1] tiene que pasar el path al fichero de mapeo de nombres de vlan
        """"

        fo = open(args[0], "r")

        self.stdout.write("Aprovisionamos las vlanes")

        self.sync_dbred_vlans(args[0])

