from models import PlanAttr
from .models import HOST
from .models import DatabaseInfraDNSList

def add_dns_record(databaseinfra, name, ip, type):
        planattr = PlanAttr.objects.get(dbaas_plan=databaseinfra.plan)
        if planattr.dnsapi_database_sufix:
            sufix = '.' + planattr.dnsapi_database_sufix
        else:
            sufix = ''

        if type == HOST:
            domain = planattr.dnsapi_vm_domain
        else:
            domain = planattr.dnsapi_database_domain
            name += sufix

        databaseinfradnslist = DatabaseInfraDNSList(
            databaseinfra = databaseinfra.id,
            name = name,
            domain = domain,
            ip = ip,
            type = type)
        databaseinfradnslist.save()

        dnsname = '%s.%s' % (name, domain)
        return dnsname
