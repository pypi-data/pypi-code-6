from __future__ import (print_function, absolute_import)
from .compat import *
from . import ca

__all__ = ['caget']

_chids = {}

def caget(pvs):
    if isinstance(pvs, basestring):
        pvs = [pvs]

    for pv in pvs:
        chid = _chids.get(pv)
        if chid is None:
            status, chid = ca.create_channel(pv)
            _chids[pv] = chid

    status = ca.pend_io(5)
    if status != ca.ECA.NORMAL:
        return

    values = {}
    for pv in pvs:
        chid = _chids.get(pv)
        status, value = ca.get(chid)
        values[pv] = value

    status = ca.pend_io(5)
    if status != ca.ECA.NORMAL:
        return

    return [values[pv].get() for pv in pvs]

