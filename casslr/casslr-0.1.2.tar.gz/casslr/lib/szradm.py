# coding:utf-8
import subprocess
import copy

from xml.etree import ElementTree


STATUS_RUNNING = "Running"


class FarmRoleException(Exception):
    pass

class FarmRoleNotFound(FarmRoleException):
    pass

class DuplicateFarmRole(FarmRoleException):
    pass


class Server(object):
    def __init__(self, index, location, internal_ip, external_ip, status):
        self.index = index
        self.location = location
        self.internal_ip = internal_ip
        self.external_ip = external_ip
        self.status = status

    @classmethod
    def from_xml(cls, xml):
        attrs = xml.attrib
        return Server(int(attrs["index"]), attrs["cloud-location"], attrs["internal-ip"], attrs["external-ip"],
                      attrs["status"])


class FarmRole(object):
    def __init__(self, id, servers):
        self.id = id
        self.servers = servers

    @classmethod
    def from_xml(cls, xml):
        id = int(xml.attrib["id"])
        servers = []
        for server_xml in xml.iterfind("./hosts/host"):
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

    def farm_role_by_id(self, farm_role_id):
        args = ["-q", "list-roles"]
        tree = self._szradm(args)

        farm_role_xml = tree.find("./roles/role[@id='{0}']".format(farm_role_id))

        if farm_role_xml is None:
            raise FarmRoleNotFound(farm_role_id)

        return FarmRole.from_xml(farm_role_xml)

    def current_farm_role_id(self):
        args = ["-q", "get-server-user-data"]
        tree = self._szradm(args)

        node = tree.find("./user-data/key[@name='farm_roleid']/value")
        id = int(node.text.strip())

        return id


