import logging
import re

from django.db import models
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import ipaddr
import simplejson
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models.signals import post_save





# Get an instance of a logger
from naman.core.pypelib import RuleTable

logger = logging.getLogger(__name__)


class MoreThanOneIfacePerVlanError(Exception):
    pass


class IfaceSequence(models.Model):
    machine = models.ForeignKey("Machine")
    vlan = models.ForeignKey("VLan")
    last_number = models.IntegerField(default=0)

    @property
    def incr(self, ):
        self.last_number += 1
        self.save()
        return self.last_number


class HostnameSequence(models.Model):
    prefix = models.CharField(max_length=11)
    last_number = models.IntegerField(default=0)

    @property
    def next(self, ):
        return self.last_number + 1

    @property
    def incr(self, ):
        self.last_number += 1
        self.save()
        return self.last_number

    def __unicode__(self, ):
        return u"%s(%s)" % (self.prefix, self.last_number)


class CICaracteristic(models.Model):
    code = models.CharField(max_length=4)
    description = models.TextField()

    def __unicode__(self, ):
        return u"%s" % self.code

    class Meta:
        abstract = True


class DNSZone(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self, ):
        return u"%s" % self.name

    def save(self, *args, **kwargs):
        new = False
        if self.pk is None:
            new = True
        super(DNSZone, self).save(*args, **kwargs)
        if new:
            logger.info("New DNSZone created: %s" % self)


class MType(models.Model):
    name = models.CharField(max_length=20)
    auto_name = models.BooleanField(default=True)
    has_serial = models.BooleanField(default=True)

    def __unicode__(self, ):
        return u"%s" % self.name


class Environment(models.Model):
    code = models.CharField(max_length=4, blank=True)
    description = models.TextField()
    backup_vlans = models.ManyToManyField('VLan', null=True, blank=True)
    service_vlans = models.ManyToManyField(
        'VLan',
        related_name='environments',
        null=True,
        blank=True)

    def __unicode__(self, ):
        return u"%s" % self.description
    
    def to_pypelib(self):
        return str(self.code)


class Role(CICaracteristic):
    needs_backup_vlan = models.BooleanField(default=False)
    
    def to_pypelib(self):
        return u"%s" % self.code


class OperatingSystem(CICaracteristic):
    def __unicode__(self, ):
        return u"%s" % self.description
    
    


class ConflictingIP(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    comments = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self, ):
        return u"%s" % self.ip


class ExcludedIPRange(models.Model):
    first = models.IPAddressField()
    last = models.IPAddressField()
    vlan = models.ForeignKey("VLan", related_name="excluded_ranges")

    class ExcludedIPError(Exception):
        pass

    def __unicode__(self, ):
        return "vlan: %s (%s - %s)" % (self.vlan, self.first, self.last)

    @property
    def as_tuple(self, ):
        return (self.first, self.last)

    def in_range(self, ip):
        if not isinstance(ip, ipaddr.IPv4Address):
            ip = ipaddr.IPv4Address(ip)

        if not isinstance(self.first, ipaddr.IPv4Address):
            self.first = ipaddr.IPv4Address(self.first)

        if not isinstance(self.last, ipaddr.IPv4Address):
            self.last = ipaddr.IPv4Address(self.last)

        if ip in self.as_tuple:
            return True

        if ip > self.first and ip < self.last:
            return True
        return False


@receiver(pre_save, sender=ExcludedIPRange)
def pre_save_excludediprange(sender, instance, **kwargs):

        if not instance.vlan.is_ip_valid(instance.first):
            raise ipaddr.AddressValueError("First IP is not correct for vlan")

        if not instance.vlan.is_ip_valid(instance.last):
            raise ipaddr.AddressValueError("Last IP is not correct for vlan")


class VLanManager(models.Manager):

    def get_from_ip(self, ip):

        for vlan in self.all():
            if vlan.is_ip_valid(ip):
                return vlan
        return None


class VLan(models.Model):
    name = models.CharField(max_length=20)
    tag = models.IntegerField()
    ip = models.IPAddressField()
    gw = models.IPAddressField()
    mask = models.IntegerField()
    management_purpose = models.BooleanField(default=False)
    provisioning_purpose = models.BooleanField(default=False)
    dhcp = models.BooleanField(default=True)
    #general_purpose_service = models.BooleanField(default=False)

    class Meta:
        ordering = ("name", )

    class NoFreeIPError(Exception):
        pass

    def __unicode__(self, ):
        return u"%s(%s)" % (self.name, self.tag)

    @property
    def info(self, ):
        hosts = [x for x in self.network.iterhosts()]
        return u"%s; first_ip: %s; last_ip: %s; num_hosts: %s" % (
            self,
            hosts[0],
            hosts[-1],
            len(hosts),
        )

    def is_ip_valid(self, ip):
        """ Calculates if an IP belongs to the vlan addressing scope"""

        if not isinstance(ip, ipaddr.IPv4Address):
            ip = ipaddr.IPv4Address(ip)
        for nip in self.network.iterhosts():
            if nip == ip:
                return True
        return False

    @property
    def network(self, ):
        try:
            return ipaddr.IPv4Network("%s/%s" % (self.ip, self.mask))
        except Exception:
            raise ValueError(
                "VLan.network: Can't calculate vlan network due to vlan %s misconfiguration" % self.name)


    @property
    def has_free_ip(self, ):
        return True if self.get_ip() else False

    def get_ip(self, ):
        """ searches and returns a free IP, respects excluded ranges and conflicting ips"""
        eranges = self.excluded_ranges
        #print "looking for an IP in scope: %s" % self.network

        for ip in self.network.iterhosts():
            #print "tryuing with: %s" % ip
            try:
                for erange in eranges.all():
                    if erange.in_range(ip):
                        raise ExcludedIPRange.ExcludedIPError
                #print "query: %s" % ConflictingIP.objects.filter(ip=ip).query
                if ConflictingIP.objects.filter(ip=str(ip)).exists():
                    continue
            except ExcludedIPRange.ExcludedIPError:
                continue
            try:
                Iface.objects.get(ip=str(ip))
            except ObjectDoesNotExist:
                return str(ip)

        return None

    def save(self, *args, **kwargs):
        new = False
        if self.pk is None:
            new = True
        super(VLan, self).save(*args, **kwargs)
        if new:
            logger.info("New VLAN created: %s" % self)


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    dmz = models.ForeignKey('VLan', null=True, blank=True)
    service_vlans = models.ManyToManyField('VLan', related_name='projects')
    #machines = models.ManyToManyField("Machine")

    def __unicode__(self, ):
        return u"%s(%s)" % (self.name, self.code)

    def save(self, *args, **kwargs):
        new = False
        if self.pk is None:
            new = True
        super(Project, self).save(*args, **kwargs)
        if new:
            logger.info("New Project created: %s" % self)
            
    def to_pypelib(self):
        return str(self.code)


class Machine(models.Model):
    hostname = models.CharField(max_length=25, blank=True, null=True)
    dns_zone = models.ForeignKey(DNSZone, blank=True, null=True)
    environment = models.ForeignKey(Environment, blank=True, null=True)
    role = models.ForeignKey(Role, blank=True, null=True)
    operating_system = models.ForeignKey(
        OperatingSystem,
        blank=True,
        null=True)
    virtual = models.BooleanField(default=False)
    project = models.ForeignKey(
        Project,
        related_name="machines",
        null=True,
        blank=True)
    mtype = models.ForeignKey(MType, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    dmz_located = models.BooleanField(default=False)
    #close_to = models.ForeignKey(Machine)

    class Meta:
        ordering = ("hostname",)

    def initialize_hostname(self, ):
        if self.role is None:
            raise AttributeError("If no hostname is specified, role must be initialized")
        if self.operating_system is None:
            raise AttributeError("If no hostname is specified, operating system must be initialized")
        if self.environment is None:
            raise AttributeError("If no hostname is specified, environment must be initialized")
        hn = u"%s%s%s%s" % (
            self.role.code,
            self.project.code if self.project is not None else "",
            self.operating_system.code,
            self.environment.code if self.environment.code != "PRO" else "",
            )
        hn = hn.lower()
        if self.mtype.has_serial:
            hn = "%s%s" % (
                hn,
                HostnameSequence.objects.get_or_create(prefix=hn)[0].incr)
        self.hostname = hn

    def initialize_dnszone(self):

        try:
            if self.operating_system.code == "w":
                self.dns_zone = DNSZone.objects.get(name=".iberia.ib")
            else:
                self.dns_zone = DNSZone.objects.get(name=".ib")

            if self.environment.code == "lab":
                self.dns_zone = DNSZone.objects.get(name=".lab")
        except AttributeError:
            pass

    def save(self, *args, **kwargs):
        new = False
        print "save hostbname: %s" % self.hostname
        with transaction.commit_on_success():
            if self.pk is None:
                new = True
                if(self.mtype is not None and
                    self.mtype.auto_name and
                    self.hostname in (None, "")
                    ):
                    self.initialize_hostname()

                elif self.hostname is None or self.hostname == "":
                    raise AttributeError(
                        "Hostname missing for a non automatic one")
                self.initialize_dnszone()

            super(Machine, self).save(*args, **kwargs)
            if new:
                logger.info("New machine created: %s" % self)

    @property
    def fqdn(self, ):
        return u"%s%s" % (self.hostname, self.dns_zone)

    def __unicode__(self, ):
        return u"%s" % self.fqdn if not self.dns_zone is None else self.hostname

    def has_iface_on_vlan(self, vlan):
        return self.interfaces.filter(vlan=vlan).exists()
    
    def get_vlanconfig(self):
        if not self.vlan_configs.count():
            self.vlan_configs.append(VLanConfig())
        return self.vlan_configs.get() 


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    iface = models.ForeignKey("Iface", related_name="services", verbose_name='Ip') #Esto permite referenciar los servicios de un iface desde un objeto Iface

    def __unicode__(self, ):
        return u"%s" % self.name


class IfaceManager(models.Manager):

    def query_cmd(self, query_string):

        m = re.match("^(.+)=(.+)$", query_string)
        if not m:
            #print "no hay coincidencia"
            return None
        try:
            print "Se ha encontrado: %s" % m.group(2)
            queriable = {
                "name": self.filter(name__iregex=m.group(2)),
                "vlan": self.filter(vlan__name__iregex=m.group(2)),
                "machines": self.filter(machines__hostname__iregex=m.group(2)),
                "ip": self.filter(ip__iregex=m.group(2)),
                "gw": self.filter(gw__iregex=m.group(2)),
                "mask": self.filter(mask__iregex=m.group(2)),
                "comments": self.filter(comments__iregex=m.group(2)),
                "mac": self.filter(mac__iregex=m.group(2)),
                "nat": self.filter(nat__iregex=m.group(2)), }
            return queriable[m.group(1)]
        except KeyError:
            pass
        return None


class Iface(models.Model):
    objects = IfaceManager()
    PREFIX = "eth"

    name = models.CharField(max_length=11, blank=True)
    vlan = models.ForeignKey(VLan)
    ip = models.GenericIPAddressField(blank=True, unique=True, null=True)
    gw = models.GenericIPAddressField(blank=True, default="0.0.0.0")
    mask = models.IntegerField(blank=True)
    machines = models.ManyToManyField(
        Machine,
        related_name="interfaces",
        null=True,
        blank=True)
    comments = models.TextField(null=True, blank=True)
    mac = models.CharField(max_length=17, null=True, blank=True)
    nat = models.GenericIPAddressField(null=True, blank=True)
    virtual = models.BooleanField(default=False)
    dhcp = models.BooleanField(default=False)

    def to_json(self, ):
        return simplejson.dumps({
            "id": self.pk,
            "ip": self.ip,
            "vlan": self.vlan.pk,
            "dhcp": self.dhcp,
            })

    def __unicode__(self, ):
        return u"%s" % self.ip if not self.ip is None else self.name if self.name != ""  else "IFACE"



    @staticmethod
    def excluded_in_ranges(ip, vlan=None):

        if vlan is None:
            vlan = Iface.find_vlan(ip)
            if vlan is None:
                return []
        exclusions = []
        for eir in ExcludedIPRange.objects.filter(vlan=vlan):
            if eir.in_range(ip):
                exclusions.append(eir)
        return exclusions

    @staticmethod
    def find_vlan(ip):
        """
        Looksup a valid vlan for the passed ip.
        if no vlan found, return None
        """
        for vlan in VLan.objects.all():
            try:
                if vlan.is_ip_valid(ip):
                    return vlan
            except ValueError:
                logger.error("VLan %s might be misconfigured, thus can't check if ip %s belongs to it" % (vlan, ip))
                continue

        return None

    def save(self, *args, **kwargs):
        new = False
        with transaction.commit_on_success():
            if self.pk is None:
                new = True
                
                self.dhcp = self.vlan.dhcp               
                
                self.ip = self.vlan.get_ip() if self.ip in (None, "") and not self.dhcp else self.ip
                #If IP comes from user, check its valid for vlan
                if not self.dhcp and not self.vlan.is_ip_valid(self.ip): raise AttributeError("Ip %s is not valid for vlan %s" % (self.ip, self.vlan))
                                    
                self.gw = self.vlan.gw
                

            self.mask = self.vlan.mask

            super(Iface, self).save(*args, **kwargs)

            if new:
                logger.info("New Iface created: %s" % self)


COND_CHOICES = (
    ('environment', 'Machine environment'),
    ('project', 'Machine project'),
    ('role_needs_backup', 'Machine role needs backup'),
    ('dmz_located', 'Machine located in DMZ'),
    ("needs_backup", "Machine needs backup"),
    ('needs_management', "Machine needs management"),
)


class Conditional(models.Model):
    statement1 = models.CharField(max_length=60,choices=COND_CHOICES, default="environment")
    statement2 = models.CharField(max_length=60, null=True, blank=True)
    #ocurred = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u"%s is %s" % (self.statement1, self.statement2)
    
    def to_pypelib(self):
        return u"(%s = %s)" % (str(self.statement1), str(self.statement2))


ACTION_CHOICES = (
    ("assign_backup_vlan", "Assign backup vlan"),
    ("assign_management_vlan", "Assign management vlan"),
    ("assign_provisioning_vlan", "Assign provisioning vlan"),
    ("assign_dmz_based_on_project", "Assign DMZ based on project"),
    ("assign_service_vlan_based_on_project", "Assign service vlan based on project"),
    ("assign_general_purpose_service_vlan", "Assign general purpose vlan"),
)

class Rule(models.Model):

    table = models.CharField(max_length=30)
    conditionals = models.ManyToManyField(Conditional, null=True, blank=True)
    #conditionals = models.CharField(max_length=65, choices=COND_CHOICES)
    action = models.CharField(max_length=65, choices=ACTION_CHOICES, null=True, blank=True)
    active = models.BooleanField(default=True)    
    terminal = models.BooleanField(default=False)
    
    def __unicode__(self, ):
        return "[%s] conditionals: %s; action: %s" % (
            self.active,

            self.conditionals.all(),
            self.action,
        )

    def to_pypelib(self, ):
        
        conds = self.conditionals.all()
        
        out = "if "
                
        if conds.count():
            out = "%s (" % out
            for c in conds:
                out = "%s %s && " % (out, c.to_pypelib())
                
            out = re.sub("&&\s$", ")", out)
        #print out
        #out = re.sub("&&$", "", out)
        if conds.count() == 0: out = "%s 1 = 1 " % out
        
        return "%s then accept %s do %s" % (out, "" if self.terminal else "nonterminal", self.action)
    
class VLanConfig(models.Model):

    machine = models.ForeignKey(Machine, related_name="vlan_configs")
    vlans = models.ManyToManyField(VLan, blank=True, null=True)
    needs_backup = models.BooleanField(default=True)
    needs_management = models.BooleanField(default=False)
    class Meta:
        verbose_name = "Configuracion de vlanes para maquina"
        verbose_name_plural = "Configuraciones de vlanes para maquinas"

    def __unicode__(self, ):
        out = u"VLan config for %s: [" % self.machine

        for vlan in self.vlans.all().order_by('name'):
            out = "%s %s," % (out, vlan)

        return u"%s]" % out

    def append_vlan(self, vlan):
        """ Adds a new vlan checking if it has free IPs """
        if not vlan.has_free_ip:
            raise VLan.NoFreeIPError(vlan)
        self.vlans.add(vlan)
        print("Vlan %s added" % vlan)


    def save(self, *args, **kwargs):

        new = (self.pk is None)

        super(VLanConfig, self).save(*args, **kwargs)

        
        
        
            
@receiver(post_save, sender=VLanConfig)
def post_save_vlanconfig(sender, instance, **kwargs):
    from naman.core.mappings import get_mappings
    from naman.core.pypelib.RuleTable import RuleTable


    if instance.machine.role is None:
        raise AttributeError("Machine %s has no role assigned" % instance.machine)
    if instance.machine.environment is None:
        raise AttributeError("Machine %s has no environment assigned" % instance.machine)

    table = RuleTable(
        "Backup, service and management",
        get_mappings(),
        "RegexParser",
        #rawfile,
        "RAWFile",
        None)

    table.setPolicy(False)
    for rule in Rule.objects.filter(active=True).order_by("pk"):
        table.addRule(rule.to_pypelib())
        
    logging.debug(table.dump())
    
    try:
        table.evaluate(instance.machine)
        logging.debug("Ha evaluado a True")
    except Exception, ex:
        import traceback
        print "Ha evaluado a False: %s" % traceback.format_exc()
        logging.debug("Table evaluated False")
        pass
    logging.debug("Vlan config saved, vlans: %s" % instance.vlans.all())
    for vlan in instance.vlans.all():
        iface = Iface(vlan=vlan)
        iface.save()
        iface.machines.add(instance.machine)


@receiver(pre_save, sender=VLanConfig)
def pre_save_vlanconfig(sender, instance, **kwargs):
    if instance.pk is None:
        #deleting possible previous vlanconfigs, only if its new
        VLanConfig.objects.filter(machine=instance.machine).delete()
