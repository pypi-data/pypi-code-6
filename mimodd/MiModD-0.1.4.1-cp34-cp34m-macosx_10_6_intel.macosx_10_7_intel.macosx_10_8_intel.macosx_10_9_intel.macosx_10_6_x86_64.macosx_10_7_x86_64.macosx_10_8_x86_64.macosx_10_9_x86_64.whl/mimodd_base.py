class Version (tuple):
    def __str__ (self):
        return '.'.join(str(d) for d in self)

__version__ = Version([0, 1, 4, 1])

def catch_sigterm (signum, frame):
    """Define package-wide behavior on SIGTERM."""

    raise RuntimeError ('Execution stopped by system.')
