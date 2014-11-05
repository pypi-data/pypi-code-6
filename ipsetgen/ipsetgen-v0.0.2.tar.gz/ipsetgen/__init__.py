from warnings import warn
import ipaddress
import subprocess


class IPSet(object):
    def __init__(self, role, ipset_cmd=None):
        if ipset_cmd is None:
            self.ipset_cmd = 'ipset'
        else:
            self.ipset_cmd = ipset_cmd
        subprocess.check_output((ipset_cmd, '-v'),
                                universal_newlines=True,
                                stdout=subprocess.DEVNULL)

        self.role = role

    def _enumerate_role_addresses(self, role=None):
        if role is None:
            _role = self.role
        else:
            _role = role

        for service in _role.services:
            for address in service.addresses:
                yield address

    def generate_set(self):
        self.destroy_set(self.role.name)
        subprocess.call((self.ipset_cmd, 'create', self.role.name, 'hash:ip'),
                        universal_newlines=True)

        ps = [subprocess.Popen(
            (self.ipset_cmd, 'add', self.role.name, addr.compressed),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            sterr=subprocess.STDOUT,
            universal_newlines=True,
            close_fds=True) for addr in self._enumerate_role_addresses()]
        [p.wait() for p in ps]
        print(subprocess.check_output(
            (self.ipset_cmd, 'list', self.role.name)))

    def destroy_set(self, set_name):
        _destroy = (self.ipset_cmd, 'destroy', set_name)
        try:
            p = subprocess.Popen(_destroy,
                                 universal_newlines=True,
                                 stderr=subprocess.PIPE)
            _, err = p.communicate()
            if 'The set with the given name does not exist' in err:
                pass
        except FileNotFoundError:
            raise FileNotFoundError(
                'Error running {}. Is ipset installed?'.format(
                    ' '.join(_destroy)))
        return True


class Role(object):
    def __init__(self, name, services):
        self.name = name
        self.services = services


class Service(object):
    def __init__(self, name, addrs=[]):
        self.name = name
        self.addresses = map(self._validate_address, addrs)

    def __str__(self):
        return self.name

    def _validate_address(self, address):
        try:
            if '/' in address:
                addr = ipaddress.ip_network(address)
            else:
                addr = ipaddress.ip_address(address)
        except ValueError:
            warn('{} is not a valid address or network, ignoring.'.format(
                address))
        return addr
