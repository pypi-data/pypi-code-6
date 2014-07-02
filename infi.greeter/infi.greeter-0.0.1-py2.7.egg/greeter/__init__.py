__import__("pkg_resources").declare_namespace(__name__)

__all__ = ['greet', 'Greeter']

import signal
from .greeter import Greeter

def greet(product, version, log_path, status_program, login_program):
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    from infi.traceback import traceback_context
    with traceback_context():
        try:
            greeter = Greeter(product, version, log_path, status_program, login_program)
            greeter.run()
        except:
            import traceback
            traceback.print_exc()
