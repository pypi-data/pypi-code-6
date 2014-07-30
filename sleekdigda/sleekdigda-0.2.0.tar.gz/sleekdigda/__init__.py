from sleekxmpp.plugins.base import register_plugin

from .errors import (XDError, XDException)
from .stanza import (Query, Resource, Option, Destination, ResourceInfo)
from .digda import XEP_Digda
from .forward import (ConnectedResource, ListeningResource)


register_plugin(XEP_Digda)


# Retain some backwards compatibility
xep_digda = XEP_Digda