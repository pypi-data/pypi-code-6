# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

from restarter.cli import main


# common exceptions

class PidfileError(EnvironmentError):
    pass


class RestartError(RuntimeError):
    pass
