__import__("pkg_resources").declare_namespace(__name__)

__all__ = ['greet', 'Greeter', 'install']

import signal
from .greeter import Greeter
from .install import install

def greet(product, version, log_path, is_installed_program, status_program, login_program):
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    greeter = Greeter(product, version, log_path, is_installed_program, status_program, login_program)
    greeter.run()
