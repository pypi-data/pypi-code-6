import pip
import subprocess
from pkg_resources import WorkingSet, DistributionNotFound
from jinja2 import Environment, PackageLoader

    #env = Environment(loader=PackageLoader('pypc', 'templates'))

    def freeze(self):
        """Returns a list of modules installed for this Package"""
        self._freeze(self.path)

    @staticmethod
    def _freeze(path):
        """Generates a list of modules installed within path's local
        context, useful for generating requirements.txt

        TODO Consider using context manager instead of chdir
        see: http://stackoverflow.com/a/431747
        """
        with Context(path) as ctx:
            pkgs = pip.get_installed_distributions()
            return sorted('%s==%s' % (p.key, p.version) for p in pkgs)

    def setup_virtualenv(self, name='venv'):
        """Performs the initial configuration and package environment setup"""
        try:
            dep = WorkingSet().require('virtualenv')
        except DistributionNotFound:            
            pip.main(['install', 'virtualenv'])
        self.activate_virtualenv(named=name)

    @as_package
    def activate_virtualenv(self, named):
        shell = os.environ["SHELL"]
        subprocess.Popen('mkvirtualenv %s' % named, executable=shell, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        'workon %s' % named
        'source %s/bin/activate' % named

    @as_package
    def install(self, dependencies=None):
        """Installs base dependencies and writes pip freeze to
        requirements.txt
        """
        for d in dependencies:
            pip.main(['install', d])
        with open('requirements.txt', 'wb') as f:
            requirements = '\n'.join(self.freeze())
            f.write(requirements)
