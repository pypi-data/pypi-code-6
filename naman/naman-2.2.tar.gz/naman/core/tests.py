"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
#from django.test import LiveServerTestCase
#from django.test import TestCase
from django.utils import unittest
from selenium.webdriver.firefox.webdriver import WebDriver
from models import *
import requests
from requests.auth import HTTPBasicAuth
import os
from django.conf import settings
from django.contrib.auth.models import User
import simplejson
from django.test.client import RequestFactory
from views import (
    ProjectViewSet,
    MachineViewSet,
    VLanViewSet,
    IfaceViewSet,
    ExcludedIPRangeViewSet)
from rest_framework.reverse import reverse
from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ImproperlyConfigured
import ipaddr


def add_iface_for_machine(machine, vlan):
    return machine.add_iface(vlan)


def add_project(name, code):

    p = Project(name=name, code=code)
    p.save()
    return p


def add_machine(project, dns_zone, env, role, os, mtype, virtual=True, dmz_located=False):
    m = Machine(
        hostname="",
        dns_zone=dns_zone,
        environment=env,
        role=role,
        operating_system=os,
        virtual=virtual,
        project=project,
        dmz_located=dmz_located,
        mtype=mtype,
    )
    m.save()

    return m


def create_iface_creation_request(user, machine, vlan, ip=None):
    requestfactory = RequestFactory()
    data = simplejson.dumps({
        "vlan": reverse("vlan-detail", args=[vlan.pk, ]),
        "ip": ip,
        "machines": [reverse("machine-detail", args=[machine["id"], ], ), ],

    })
    request = requestfactory.post(
        reverse("iface-list"),
        data=data,
        content_type="application/json", )

    request.user = user
    request.session = {}
    print data
    return request


def create_machine_creation_request(user, project, dns_zone, env, role, os, hostname=None, mtype=None):
    requestfactory = RequestFactory()

    project = reverse(
        "project-detail",
        args=[project.pk, ]) if project is not None else ""

    data = simplejson.dumps({
        "project": project,
        "role": reverse("role-detail", args=[role.pk, ]),
        "operating_system": reverse(
            "operatingsystem-detail",
            args=[os.pk, ]),
        "environment": reverse(
            "environment-detail",
            args=[env.pk, ]),
        "dns_zone": reverse("dnszone-detail", args=[dns_zone.pk, ]),
        "mtype": reverse("mtype-detail", args=[mtype.pk, ]),
        "hostname": hostname,
    })

    request = requestfactory.post(
        reverse("machine-list"),
        data=data,
        content_type="application/json", )

    request.user = user
    request.session = {}

    return request


def add_vlan(name, tag, ip, gw, mask=24):
    v = VLan(
        name=name,
        tag=tag,
        ip=ip,
        gw=gw,
        mask=mask,
    )
    v.save()
    return v


def add_os(code, descr):
    os = OperatingSystem(
        code=code,
        description=descr,
    )
    os.save()
    return os


def add_role(code, descr):
    r = Role(
        code=code,
        description=descr,
    )
    r.save()
    return r


def add_env(code, descr):
    e = Environment(
        code=code,
        description=descr
    )
    e.save()
    return e


def add_dnszone(name):
    dz = DNSZone(name=name)
    dz.save()
    return dz


def add_mtype(name, auto_name, has_serial):
    mt = MType(name=name, auto_name=auto_name, has_serial=has_serial)
    mt.save()

    return mt


def add_superuser(name, password):
    u = User(username=name, password=password, is_superuser=True)
    u.save()
    return u


def create_excluded_ip_range_request(user, first, last, vlan):
    requestfactory = RequestFactory()
    data = simplejson.dumps({
        "vlan": reverse("vlan-detail", args=[vlan.pk, ]),
        "first": first,
        "last": last,
    })
    request = requestfactory.post(
        reverse("excludediprange-list"),
        data=data,
        content_type="application/json", )

    request.user = user
    request.session = {}
    print data
    return request


class MachineTest(TestCase):

    def setUp(self, ):
        self.factory = RequestFactory()
        self.z_ib = add_dnszone(".ib")
        self.env_pro = add_env("PRO", "production")
        self.env_pre = add_env("PRE", "preproduction")
        self.env_des = add_env("DES", "development")
        self.role_bd = add_role("BD", "base de datos")
        self.role_bd.needs_backup_vlan = True
        self.role_bd.save()

        self.role_sa = add_role("SA", "Servidor aplicaciones")
        self.role_sw = add_role("SW", "Servidor Web")
        self.role_ut = add_role("UT", "Utils server")
        self.role_ce = add_role("CE", "Conmutador Electronico")
        self.role_bal = add_role("BL", "Load Balancer")
        self.os_lin = add_os("L", "GNU/Linux")
        self.os_win = add_os("W", "Windows")

        self.mtype_server = add_mtype(
            "server",
            auto_name=True,
            has_serial=True)
        self.mtype_router = add_mtype(
            "router",
            auto_name=False,
            has_serial=False)
        self.mtype_server_standalone = add_mtype(
            "server_standalone",
            auto_name=True,
            has_serial=False)

        self.vlan_man1 = add_vlan(
            "MAN1",
            200,
            "172.21.200.0",
            "172.21.200.1",
            23,
        )
        self.vlan_patio = add_vlan(
            "PATIO",
            229,
            "172.21.228.0",
            "172.21.228.1",
            23,
        )
        self.project_ibcom = add_project("IBC", "IBC")
        self.project_crm = add_project("CRM", "CRM")
        try:

            self.user = User.objects.get(username="raton")
        except:
            self.user = add_superuser("raton", "r")

    def test_find_ip_exclusion(self, ):
        ExcludedIPRange.objects.all().delete()
        eir = ExcludedIPRange(
            first="172.21.229.1",
            last="172.21.229.10",
            vlan=self.vlan_patio,
        )
        eir.save()

        self.assertEquals(
            Iface.excluded_in_ranges("172.21.229.5"),
            [eir, ],
            "Not properly finding Excluded IP Ranges for IP 172.21.229.5, should: %s" % eir,
        )

        eir1 = ExcludedIPRange(
            first="172.21.229.8",
            last="172.21.229.12",
            vlan=self.vlan_patio,
        )
        eir1.save()

        self.assertEquals(
            Iface.excluded_in_ranges("172.21.229.9"),
            [eir, eir1, ],
            "Not properly finding Excluded IP Ranges for IP 172.21.229.9, should: %s" % [eir, eir1, ],
        )

        self.assertEquals(
            Iface.excluded_in_ranges("172.21.210.9"),
            [],
            "Not properly finding Excluded IP Ranges for IP 172.21.210.9, should None" % [eir, eir1, ],
        )

    def test_excluded_ip_ranges(self, ):

        #create an ip range who's first IP is not suitable for the assigned vlan
        request = create_excluded_ip_range_request(
            self.user,
            "172.21.200.10",
            "172.21.229.10",
            self.vlan_patio)

        func = ExcludedIPRangeViewSet.as_view({"post": "create"})
        self.assertRaises(
            ipaddr.AddressValueError,
            func, request,
            "creating an excluded ip range, not properly checking if first ip is valid for assigned vlan")

        #create an ip range who's second IP is not suitable for the assigned vlan
        request = create_excluded_ip_range_request(
            self.user,
            "172.21.229.10",
            "172.21.200.10",
            self.vlan_patio)

        self.assertRaises(
            ipaddr.AddressValueError,
            func, request,
            "creating an excluded ip range, not properly checking if second ip is valid for assigned vlan")

        #create an ip range correctly for vlan addressing with one IP
        request = create_excluded_ip_range_request(
            self.user,
            "172.21.228.10",
            "172.21.228.10",
            self.vlan_patio)

        response = (ExcludedIPRangeViewSet.as_view({"post": "create"})(request)).render()
        eir = simplejson.loads(response.content)

        self.assertEquals(
            201,
            response.status_code,
            "Is not properly creating excluded_ip_ranges (single IP)")

        #create an ip range correctly for vlan addressing with more than one IP
        request = create_excluded_ip_range_request(
            self.user,
            "172.21.228.1",
            "172.21.228.8",
            self.vlan_patio)

        response = (ExcludedIPRangeViewSet.as_view({"post": "create"})(request)).render()
        eir = simplejson.loads(response.content)
        self.assertEquals(
            201,
            response.status_code,
            "Is not properly creating excluded_ip_ranges (more than one IP)")

        #does it respect excluded ranges at iface creation??
        request = create_machine_creation_request(
            self.user,
            None,
            self.z_ib,
            self.env_pro,
            self.role_bd,
            self.os_lin,
            mtype=self.mtype_server)
        machine = simplejson.loads(
            (MachineViewSet.as_view({"post": "create"})(request)).render().content)

        request = create_iface_creation_request(
            self.user,
            machine,
            self.vlan_patio)
        print request
        response = IfaceViewSet.as_view({"post": "create"})(request)
        iface = simplejson.loads(response.render().content)

        print iface
        self.assertEquals(
            iface["ip"],
            "172.21.228.9",
            "Creating an iface is not looking at created excluded_ip_ranges")

        request = create_iface_creation_request(
            self.user,
            machine,
            self.vlan_patio)

        response = IfaceViewSet.as_view({"post": "create"})(request)
        iface = simplejson.loads(response.render().content)

        print iface
        self.assertEquals(
            iface["ip"],
            "172.21.228.11",
            "Creating an iface is not looking at created excluded_ip_ranges")

    def off_test_many_machines_for_one_iface(self, ):
        #TODO write test_many_machines_for_one_iface
        request = create_machine_creation_request(
            self.user,
            None,
            self.z_ib,
            self.env_pro,
            self.role_bd,
            self.os_lin,
            mtype=self.mtype_server)
        machine1 = simplejson.loads(
            (MachineViewSet.as_view({"post": "create"})(request)).render().content)

        request = create_machine_creation_request(
            self.user,
            None,
            self.z_ib,
            self.env_pro,
            self.role_bd,
            self.os_lin,
            mtype=self.mtype_server)
        machine2 = simplejson.loads(
            (MachineViewSet.as_view({"post": "create"})(request)).render().content)

        request = create_iface_creation_request(
            self.user,
            machine1,
            self.vlan_man1)
        response = IfaceViewSet.as_view({"post": "create"})(request)

        iface = simplejson.loads(response.render().content)

        requestfactory = RequestFactory()
        data = simplejson.dumps({
            "machine": reverse("iface-detail", args=[machine1["id"], ]),
        })
        request = requestfactory.post(
            reverse("iface-list"),
            data=data,
            content_type="application/json", )

        request.user = user
        request.session = {}
        print data

    def test_interface_rest(self, ):
        #regular iface creation with IP
        request = create_machine_creation_request(
            self.user,
            None,
            self.z_ib,
            self.env_pro,
            self.role_bd,
            self.os_lin,
            mtype=self.mtype_server)
        machine = simplejson.loads(
            (MachineViewSet.as_view({"post": "create"})(request)).render().content)

        request = create_iface_creation_request(
            self.user,
            machine,
            self.vlan_man1,
            "6.6.6.6",)

        response = IfaceViewSet.as_view({"post": "create"})(request)
        response.render()
        self.assertEquals(
            201,
            response.status_code,
            "Not properly creating iface. (should: 201; does: %s) %s" %
                  (response.status_code, response.content))

        self.assertEquals(
            simplejson.loads(response.content)["ip"],
            "6.6.6.6",
            "Not properly creating ifaces when IP is assigned by user")

        # creating the same vlan for the same machine, should create it
        request = create_iface_creation_request(
            self.user,
            machine,
            self.vlan_man1)
        response = IfaceViewSet.as_view({"post": "create"})(request)
        self.assertEquals(
            201,
            response.status_code,
            "Not properly creating second iface on same machine and vlan. (should: 201; does: %s): %s" %
                (response.status_code, response.render().content))

        #regular iface creation without IP
        request = create_iface_creation_request(
            self.user,
            machine,
            self.vlan_man1)

        response = IfaceViewSet.as_view({"post": "create"})(request)
        response.render()
        self.assertEquals(
            201,
            response.status_code,
            "Not properly creating iface. (should: 201; does: %s) %s" %
                (response.status_code, response.content))

    def test_conflicting_ip(self, ):
        Iface.objects.all().delete()
        ExcludedIPRange.objects.filter(vlan=self.vlan_man1).delete()
        ConflictingIP(ip="172.21.200.1").save()
        ip = self.vlan_man1.get_ip()
        self.assertEquals(
            ip,
            "172.21.200.2",
            "Not properly assigning an IP when there is a conflicting one. (should: 172.21.200.2, does: %s)" % ip
        )

    def test_find_vlan_for_ip(self, ):
        VLan.objects.all().delete()
        vlan_servicio = add_vlan(
            "SERVICIO",
            100,
            "172.21.100.0",
            "172.21.100.1",
            24,
        )

        vlan = Iface.find_vlan("192.168.1.1")
        self.assertIsNone(
            vlan,
            "Should return None because no 192.168.1.1 does not belong to any vlan, returned: %s" % vlan
        )

        self.assertEqual(
            vlan_servicio,
            Iface.find_vlan("172.21.100.3"),
            "Should return %s as 172.21.100.3 belongs to it" % vlan_servicio
        )

    def test_vlan_decision(self, ):
        #cleaning ifaces *******************************
        Iface.objects.all().delete()

        vlan_servicio = add_vlan(
            "SERVICIO",
            100,
            "172.21.100.0",
            "172.21.100.1",
            30,
        )

        vlan_dmz = add_vlan(
            "DMZ",
            101,
            "172.21.101.0",
            "172.21.101.1",
            30,
        )

        vlan_management = add_vlan(
            "MNG",
            102,
            "172.21.102.0",
            "172.21.102.1",
            30,
        )
        vlan_management.management_purpose = True
        vlan_management.save()

        print vlan_management.info

        vlan_project = add_vlan(
            "PROJECT",
            103,
            "172.21.103.0",
            "172.21.103.1",
            30,
        )
        vlan_backup_prod = add_vlan(
            "backup_prod",
            104,
            "172.21.104.0",
            "172.21.104.1",
            30,
        )
        vlan_backup_des = add_vlan(
            "backup_des",
            105,
            "172.21.105.0",
            "172.21.105.1",
            30,
        )

        vlan_pre = add_vlan(
            "pre",
            106,
            "172.21.106.0",
            "172.21.106.1",
            30,)

        self.env_des.backup_vlans.add(vlan_backup_des)
        self.env_pre.service_vlans.add(vlan_pre)
        self.env_pre.backup_vlans.add(vlan_backup_des)
        self.env_pro.backup_vlans.add(vlan_backup_prod)
        self.env_pro.service_vlans.add(vlan_servicio)

        project = add_project('Federation Project', 'fed')
        project.service_vlans.add(vlan_project)
        project.dmz = vlan_dmz
        project.save()

        #creating vlan config
        #  project machine
        #  campus network
        #  production
        #  role BD

        # should assign vlans: vlan_project, vlan_backup_prod, vlan_management
        m1 = add_machine(
            project,
            self.z_ib,
            self.env_pro,
            self.role_bd,
            self.os_lin,
            self.mtype_server,
            True,
            False)

        vc = VLanConfig(
            machine=m1,
            needs_backup=True,
            needs_management=True,
        )

        vc.save()
        print m1
        print vc.vlans.all().order_by('name')
        self.assertEquals(
            [vlan_management, vlan_project, vlan_backup_prod, ],
            [x for x in vc.vlans.all().order_by('name')],
            "Should have vlan_backup_prod, vlan_management, vlan_project")

        for v in vc.vlans.all():
            i = Iface(vlan=v)
            i.save()
            i.machines.add(m1)

        #creating second vlan config
        #  project machine
        #  campus network
        #  production
        #  role BD

        # should assign vlans: vlan_project, vlan_backup_prod, vlan_management
        m1 = add_machine(
            project,
            self.z_ib,
            self.env_pro,
            self.role_bd,
            self.os_lin,
            self.mtype_server,
            True,
            False)

        vc = VLanConfig(
            machine=m1,
            needs_backup=True,
            needs_management=True,
        )

        vc.save()

        self.assertEquals(
            [vlan_management, vlan_project, vlan_backup_prod, ],
            [x for x in vc.vlans.all().order_by('name')],
            "Should have vlan_backup_prod, vlan_management, vlan_project")

        for v in vc.vlans.all():
            i = Iface(vlan=v)
            i.save()
            i.machines.add(m1)

        #creating third vlan config
        #  project machine
        #  campus network
        #  production
        #  role BD

        # should not find free IPs
        m1 = add_machine(
            project,
            self.z_ib,
            self.env_pro,
            self.role_bd,
            self.os_lin,
            self.mtype_server,
            True,
            False)

        vc = VLanConfig(
            machine=m1,
            needs_backup=True,
            needs_management=True,
        )
        func = vc.save
        self.assertRaises(
            VLan.NoFreeIPError,
            func,
            "Should raise NoFeeIPError as there are no free IPs"
        )

        #cleaning ifaces *******************************
        Iface.objects.all().delete()

        #creating vlan config
        #  NON project machine
        #  campus network
        #  production
        #  role SA(no backup needed)

        # should assign vlans: vlan_servicio, vlan_management
        m1 = add_machine(
            None,
            self.z_ib,
            self.env_pro,
            self.role_sa,
            self.os_lin,
            self.mtype_server,
            True,
            False)

        vc = VLanConfig(
            machine=m1,
            needs_backup=True,
            needs_management=True,
        )

        vc.save()
        self.assertEquals(
            [vlan_management, vlan_servicio, ],
            [x for x in vc.vlans.all().order_by('name')],
            "Should have vlan_servicio and vlan_management")

        Iface(vlan=vlan_servicio).save()
        Iface(vlan=vlan_servicio).save()
        #creating vlan config
        #  NON project machine
        #  campus network
        #  production
        #  role SA(no backup needed)

        # should not find free IPs for vlan_servicio
        m1 = add_machine(
            None,
            self.z_ib,
            self.env_pro,
            self.role_bd,
            self.os_lin,
            self.mtype_server,
            True,
            False)

        vc = VLanConfig(
            machine=m1,
            needs_backup=True,
            needs_management=True,)

        func = vc.save
        self.assertRaises(
            VLan.NoFreeIPError,
            func,
            "It should find free IPs for vlan_servicio, but it did")
        #cleaning ifaces *******************************
        Iface.objects.all().delete()

        Iface(vlan=vlan_backup_prod).save()
        Iface(vlan=vlan_backup_prod).save()
        #creating vlan config
        #  NON project machine
        #  campus network
        #  production
        #  role SA(no backup needed)

        # should not find free IPs for vlan_backup
        m1 = add_machine(
            None,
            self.z_ib,
            self.env_pro,
            self.role_bd,
            self.os_lin,
            self.mtype_server,
            True,
            False)

        vc = VLanConfig(
            machine=m1,
            needs_backup=True,
            needs_management=True,)

        func = vc.save
        self.assertRaises(
            VLan.NoFreeIPError,
            func,
            "It should find free IPs for vlan_backup_prod, but it did")

        #cleaning ifaces *******************************
        Iface.objects.all().delete()

        #creating vlan config
        #  NON project machine
        #  campus network
        #  pre
        #  role SA(no backup needed)

        # should not find free IPs for vlan_backup
        m1 = add_machine(
            None,
            self.z_ib,
            self.env_pre,
            self.role_sa,
            self.os_lin,
            self.mtype_server,
            True,
            False)

        vc = VLanConfig(
            machine=m1,
            needs_backup=True,
            needs_management=True,)

        vc.save()
        self.assertEquals(
            2,
            vc.vlans.all().count(),
            "Should onkly have 2 vlans, as role needs no backup")

        self.assertEquals(
            [vlan_management, vlan_pre, ],
            [x for x in vc.vlans.all().order_by('name')],
            "Should have vlan_pre and vlan_management")

        #creating vlan config
        #  project machine
        #  DMZ network
        #  pro
        #  role SA(no backup needed)

        # should assign [vlan_management, vlan_dmz]
        m1 = add_machine(
            project,
            self.z_ib,
            self.env_pro,
            self.role_sa,
            self.os_lin,
            self.mtype_server,
            True,
            True)

        vc = VLanConfig(
            machine=m1,
            needs_backup=True,
            needs_management=True,)

        vc.save()
        self.assertEquals(
            2,
            vc.vlans.all().count(),
            "Should onkly have 2 vlans, as role needs no backup")

        self.assertEquals(
            [vlan_dmz, vlan_management, ],
            [x for x in vc.vlans.all().order_by('name')],
            "Should have vlan_dmz and vlan_management; does: %s" % vc)

        #creating vlan config
        #  NON project machine
        #  DMZ network
        #  pro
        #  role SA(no backup needed)

        # should raise ImproperConfigured Exception because system
        # can't find dmz for non-project machine
        m1 = add_machine(
            None,
            self.z_ib,
            self.env_pro,
            self.role_sa,
            self.os_lin,
            self.mtype_server,
            True,
            True)

        vc = VLanConfig(
            machine=m1,
            needs_backup=True,
            needs_management=True,)

        func = vc.save
        self.assertRaises(
            ImproperlyConfigured,
            func,
            "Should raise ImproperlyConfigured because system can't allocate dmz for non-project machine")

        #creating vlan config
        #  project machine
        #  DMZ network
        #  pro
        #  role BD

        # should [vlan_dmz, vlan_backup, vlan_management]
        m1 = add_machine(
            project,
            self.z_ib,
            self.env_pro,
            self.role_bd,
            self.os_lin,
            self.mtype_server,
            True,
            True)

        vc = VLanConfig(
            machine=m1,
            needs_backup=True,
            needs_management=True,)

        vc.save()
        self.assertEquals(
            3,
            vc.vlans.all().count(),
            "Should have 3 vlans, as role needs backup")

        self.assertEquals(
            [vlan_dmz, vlan_management, vlan_backup_prod],
            [x for x in vc.vlans.all().order_by('name')],
            "Should have vlan_dmz and vlan_management; does: %s" % vc)

    def test_standalone_hostnames_rest(self, ):

        #creating a regular server for CRM project
        request = create_machine_creation_request(
            self.user,
            self.project_crm,
            self.z_ib,
            self.env_des,
            self.role_bd,
            self.os_lin,
            mtype=self.mtype_server,
        )
        response = MachineViewSet.as_view({"post": "create"})(request).render()
        proper_name = ("%s%s%s%s1" % (
            self.role_bd.code,
            self.project_crm.code,
            self.os_lin.code,
            self.env_des.code)).lower()

        machine = simplejson.loads(response.content)
        self.assertEquals(
            proper_name,
            machine["hostname"],
            "Not properly creating cluster server hostname (should: %s; does: %s)" % (
                proper_name,
                machine["hostname"],
            )
        )
        #creating an standalone server once already exists a regular server with same properties
        request = create_machine_creation_request(
            self.user,
            self.project_crm,
            self.z_ib,
            self.env_des,
            self.role_bd,
            self.os_lin,
            mtype=self.mtype_server_standalone
        )
        response = MachineViewSet.as_view({"post": "create"})(request).render()
        proper_name = ("%s%s%s%s" % (
            self.role_bd.code,
            self.project_crm.code,
            self.os_lin.code,
            self.env_des.code)).lower()

        machine = simplejson.loads(response.content)
        self.assertEquals(
            proper_name,
            machine["hostname"],
            "Not properly creating standalone server hostname when a cluster server exist for the same properties (should: %s; does: %s)" % (
                proper_name,
                machine["hostname"],
            )
        )

        #creating the second regular server once already exists a
        #regular server and a standalone server with same properties
        request = create_machine_creation_request(
            self.user,
            self.project_crm,
            self.z_ib,
            self.env_des,
            self.role_bd,
            self.os_lin,
            mtype=self.mtype_server
        )
        response = MachineViewSet.as_view({"post": "create"})(request).render()
        proper_name = ("%s%s%s%s2" % (
            self.role_bd.code,
            self.project_crm.code,
            self.os_lin.code,
            self.env_des.code)).lower()

        machine = simplejson.loads(response.content)
        self.assertEquals(
            proper_name,
            machine["hostname"],
            "Not properly creating hostnames (should: %s; does: %s)" % (
                proper_name,
                machine["hostname"],
            )
        )

    def off_test_no_auto_name(self, ):

        #creating machine without autoname and not sending hostname
        request = create_machine_creation_request(
            self.user,
            None,
            self.z_ib,
            self.env_pro,
            self.role_ce,
            self.os_lin,
            mtype=self.mtype_router)

        try:
            MachineViewSet.as_view({"post": "create"})(request)
            assert("No properly creating machine with no auto name. No hostname has been sent, it should return 400, does: %s" % response.status_code)
        except IntegrityError:
            pass

        #creating machine that should increment counter
        request = create_machine_creation_request(
            self.user,
            self.project_ibcom,
            self.z_ib,
            self.env_des,
            self.role_bd,
            self.os_lin,
            mtype=self.mtype_server)

        response = MachineViewSet.as_view({"post": "create"})(request).render()
        self.assertEquals(
            201,
            response.status_code,
            "Not properly return status after machine creation(should:201;does:%s" % response.status_code)

        proper_name = ("%s%s%s%s1" % (
            self.role_bd.code,
            self.project_ibcom.code,
            self.os_lin.code,
            self.env_des.code)).lower()

        machine = simplejson.loads(response.content)
        self.assertEquals(
            proper_name,
            machine["hostname"],
            "Not properly creating hostnames (should: %s; does: %s)" % (
                proper_name,
                machine["hostname"],
            )
        )

        # creating machine that needs a specified hostname, even though there is
        # a previous cluster server with same properties
        request = create_machine_creation_request(
            self.user,
            self.project_ibcom,
            self.z_ib,
            self.env_des,
            self.role_bd,
            self.os_lin,
            mtype=self.mtype_server_standalone,
            hostname="bdibcldes")

        response = MachineViewSet.as_view({"post": "create"})(request).render()
        self.assertEquals(
            201,
            response.status_code,
            "Not properly return status after machine creation(should:201;does:%s)" % response.status_code)

        proper_name = "bdibcldes"

        machine = simplejson.loads(response.content)
        self.assertEquals(
            proper_name,
            machine["hostname"],
            "Not properly creating hostnames (should: %s; does: %s)" % (
                proper_name,
                machine["hostname"],
            )
        )
        #creating the other cluster machine
        request = create_machine_creation_request(
            self.user,
            self.project_ibcom,
            self.z_ib,
            self.env_des,
            self.role_bd,
            self.os_lin,
            mtype=self.mtype_server)

        response = MachineViewSet.as_view({"post": "create"})(request).render()
        self.assertEquals(
            201,
            response.status_code,
            "Not properly return status after machine creation(should:201;does:%s" % response.status_code)

        proper_name = ("%s%s%s%s2" % (
            self.role_bd.code,
            self.project_ibcom.code,
            self.os_lin.code,
            self.env_des.code)).lower()

        machine = simplejson.loads(response.content)
        self.assertEquals(
            proper_name,
            machine["hostname"],
            "Not properly creating hostnames (should: %s; does: %s)" % (
                proper_name,
                machine["hostname"],
            )
        )

    def test_alta_router(self, ):
        request = create_machine_creation_request(
            self.user,
            None,
            self.z_ib,
            self.env_pro,
            self.role_ce,
            self.os_lin,
            mtype=self.mtype_router,
            hostname="CE_MAN1"
        )
        response = MachineViewSet.as_view({"post": "create"})(request).render()
        self.assertEquals(
            201,
            response.status_code,
            "Not properly return status after machine creation(should:201;does:%s" % response.status_code)

        machine = simplejson.loads(response.content)
        self.assertEquals(
            "CE_MAN1",
            machine["hostname"],
            "Not properly creating hostnames (should: %s; does: %s)" % (
                "CE_MAN1",
                machine["hostname"],
            )
        )



    def test_alta_balanceador(self, ):
        request = create_machine_creation_request(
            self.user,
            None,
            self.z_ib,
            self.env_pro,
            self.role_bal,
            self.os_lin,
            mtype=self.mtype_router,
            hostname="bigip1"
        )
        response = MachineViewSet.as_view({"post": "create"})(request).render()
        self.assertEquals(
            201,
            response.status_code,
            "Not properly return status after load balancer creation(should:201;does:%s" % response.status_code)
        machine = simplejson.loads(response.content)
        self.assertEquals(
            machine["hostname"],
            "bigip1",
            "Not properly initializing load balancer hostname",
        )
