# -*- coding: utf-8 -*-
from naman.core.models import *
from django.db import connections, DatabaseError
redip = connections['redip'].cursor()
bahamas = connections['bahamas'].cursor()


class Command(BaseCommand):
    args = ''
    help = """

"""

    def handle(self, *args, **options):
        print args
        fo = open(args[0], "r")

   #     dns_zone = DNSZone.objects.get(name="undefined")
   #     environment = Environment.objects.get(code="unde")
   #     role = Role.objects.get(code="unde")
   #     os = OperatingSystem.objects.get(code="unde")
   #     mtype = MType.objects.get(name="imported")
        self.stdout.write("Aprovisionamos las vlanes")
        query = "select * from vlans"
        bahamas.execute(query)
        for row in bahamas.fetchall():
            VLan.objects.get_or_create(
                name=row[3],
                mask=row[4],
                ip=row[10],
                tag=0,
                gw=row[1],
            )

        self.stdout.write("Aprovisionamos las maquinas")
        for table in fo.readlines():
            table = table.replace("\n", "")
            self.stdout.write("Trabajamos con la tabla: %s" % table)
            query = "SELECT systemName, location FROM %s" % table
            self.stdout.write("query: %s" % query)

            try:
                redip.execute(query)
            except UnicodeDecodeError:
                self.stderr.write("ERROR: Tabla %s con fallos unicode" % table)
                continue

            for row in redip.fetchall():
                if row[0] not in ("", None):
                    try:
                        location = row[1]
                    except Exception:
                        location = None

                    if row[0] in (None, ""):
                        continue
                    print "metemos la maquina: %s" % row[0]
                    try:
                        m = Machine.objects.get(hostname=row[0])
                    except Machine.DoesNotExist:
                        Machine(hostname=row[0].lower()).save()


        fo.seek(0)
        self.stdout.write("Aprovisionamos las interfaces")
        for table in fo.readlines():
            hay_nat = True
            table = table.replace("\n", "")
            self.stdout.write("Trabajamos con la tabla: %s" % table)
            try:
                vlan = VLan.objects.get(name=table)
            except VLan.DoesNotExist:
                self.stderr.write("El fichero de tablas muestra la tabla %s, pero no existe" % table )
                continue

            query = "SELECT address, systemName, comments, nat FROM %s where status= 'Used'" % table

            try:
                redip.execute(query)

            except DatabaseError:
                query = "SELECT address, systemName, comments FROM %s where status= 'Used'" % table
                redip.execute(query)
                hay_nat = False
            except UnicodeDecodeError:
                self.stderr.write("ERROR: Tabla %s con fallos unicode" % table)
                continue

            for iface in redip.fetchall():
                machine = Machine.objects.get(hostname=iface[1])
                nat = row[3] if hay_nat else None
                niface = Iface(
                    name="migrated",
                    vlan=vlan,
                    ip=iface[0],
                    comments=iface[2],
                    nat=nat)
                niface.save()
                niface.machines.add(machine)

        fo.close()

