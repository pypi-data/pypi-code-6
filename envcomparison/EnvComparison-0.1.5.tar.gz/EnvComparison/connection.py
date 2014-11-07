from paramiko import SSHClient, SSHConfig, AutoAddPolicy
import re
import pprint


class Connection(object):
    
    def __init__(self, config_location, server_name):


        self.system = {}
        self.system['ssh_hostname'] = server_name

        config = SSHConfig()
        config.parse(open(config_location))
        o = config.lookup(server_name)

        self.ssh_client = SSHClient()
        self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh_client.load_system_host_keys()
        self.ssh_client.connect(o['hostname'], username=o['user'], key_filename=o['identityfile'])


    def _run_command(self, cmd):
        """
        Run a remote command and gather output
        """
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        return stdout.readlines()

        
    def _check_command(self, cmd):
        """ 
        Run a remote command and get the exit status
        """
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        return stdout.channel.recv_exit_status()


    def system_check(self):
        """
        Should do something with this test one day...
        """
        if self._check_command('file') != 1:
            pass
        if self._check_command('which') != 1:
            pass

    def get_platform_family(self):
        """
        Get platform family
        """
        if self.system['platform'] in ['oracle', 'centos', 'redhat', 'scientific', 'enterpriseenterprise', 'amazon']:
            self.system['platform_family'] = 'rhel'
        if self.system['platform'] in ['debian', 'ubuntu', 'linuxmint']:
            self.system['platform_family'] = 'debian'
        if self.system['platform'] in ['fedora']:
            self.system['platform_family'] = 'fedora'

    def get_system_packages(self):
        """ 
        Get packages installed through the default pakacga manager
        """
        self.packages = {}
        if self.system['platform_family'] == 'debian':
            for line in self._run_command('dpkg -l'): # parse dpkg -l or /var/lib/dpkg/status ??? 
                parts = line.split()
                if parts[0] == 'ii':
                    self.system['system-package-' + str(parts[1])] = parts[2]

        elif self.system['platform_family'] == 'rhel':
            pass

        elif self.system['platform_family'] == 'arch':
            pass

        #elif self.system['platform_family'] == '':

        #else:
        #    self.system['platform_family'] == 


        #self.system['packages'] = self.packages


    def get_platform_details(self):
        """
        is ubuntu? 
        """
        avars = self._run_command('lsb_release -a')

        final = ' '.join(avars).lower()
        output = dict(re.findall(r'(\S[^:]+):\s*(.*\S)', final))
        self.system['platform'] = output['distributor id']
        self.system['codename'] = output['codename']
        self.system['release'] = output['release']



    def get_system_arch(self):
        self.system['arch'] = self._run_command('arch')[0].strip()


        
    def get_fqdn(self):
        """
        Get the fully qualified domain name
        """
        self.system['fqdn'] = self._run_command('hostname --fqdn')[0].strip()


    def get_pip_packages(self):
        """
        Get packages installed to Global PIP
        """
        if self._check_command('which pip') == 0:
            for line in self._run_command('pip freeze'):
                if '==' in line:
                    parts = line.strip().split('==')
                    self.system['pip-package-' + str(parts[0])] = parts[1] 

        
    def get_php_packages(self):
        """
        Get globally installed PHP packages
        """
        if self._check_command('which php') == 0:
            for line in self._run_command('php -i | grep -i "version =>"'):
                parts = line.strip().split(' => ')
                self.system['php-package-' + str(parts[0])] = parts[1]


    def get_ruby_packages(self):
        """
        Get globally installed Ruby packages
        """
        if self._check_command('which gem') == 0:
            for line in self._run_command('gem list | grep -i "(\|)"'):
                parts = line.strip().split(' ')
                parts[1] = parts[1].replace('(','').replace(')','')
                self.system['ruby-package-' + str(parts[0])] = parts[1]



    def pretty_print(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.system)


