# coding:utf-8
import subprocess
import functools
import copy

from xml.etree import ElementTree


STATUS_RUNNING = "Running"


class SzradmException(Exception):
    pass

class FarmRoleException(SzradmException):
    pass

class FarmRoleNotFound(FarmRoleException):
    pass

class DuplicateFarmRole(FarmRoleException):
    pass

class InvalidDataReturned(SzradmException):
    pass


def wrap_value_errors(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            raise SzradmException(e.message)
    return wrapper


class Server(object):
    def __init__(self, index, location, internal_ip, external_ip, status):
        self.index = index
        self.location = location
        self.internal_ip = internal_ip
        self.external_ip = external_ip
        self.status = status

    @classmethod
    @wrap_value_errors
    def from_xml(cls, xml):
        attrs = xml.attrib
        return Server(int(attrs["index"]), attrs["cloud-location"], attrs["internal-ip"], attrs["external-ip"],
                      attrs["status"])


class FarmRole(object):
    def __init__(self, id, servers):
        self.id = id
        self.servers = servers

    @classmethod
    @wrap_value_errors
    def from_xml(cls, xml):
        id = int(xml.attrib["id"])
        servers = []
        for server_xml in xml.findall("./hosts/host"):
            servers.append(Server.from_xml(server_xml))
        return FarmRole(id, servers)

    @property
    def running_servers(self):
        for server in self.servers:
            if server.status == STATUS_RUNNING:
                yield server

    def __str__(self):
        return "<FarmRole: {0}>".format(self.id)


class FarmRoleEngine(object):
    def _szradm(self, params):
        """
        Make a call to szradm, check for errors, and return the output
        """

        params = copy.copy(params)
        params.insert(0, "/usr/local/bin/szradm")
        proc = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.wait():
            raise FarmRoleException("Unable to access szradm: %s", proc.stderr.read())
        return ElementTree.parse(proc.stdout)

    @wrap_value_errors
    def farm_role_by_id(self, farm_role_id):
        args = ["-q", "list-roles"]
        tree = self._szradm(args)

        # No XPath here: Python 2.6 support
        for farm_role_xml in tree.findall("./roles/role"):
            if int(farm_role_xml.attrib.get("id")) == farm_role_id:
                return FarmRole.from_xml(farm_role_xml)

        raise FarmRoleNotFound(farm_role_id)


    @wrap_value_errors
    def current_farm_role_id(self):
        args = ["-q", "get-server-user-data"]
        tree = self._szradm(args)

        # Same as above re: XPath
        for udk_xml in tree.findall('./user-data/key'):
            if udk_xml.attrib.get("name") == "farm_roleid":
                return int(udk_xml.find('value').text.strip())

        raise InvalidDataReturned("No farm_roleid user-data key found")

