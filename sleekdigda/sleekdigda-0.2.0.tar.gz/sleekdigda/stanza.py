from sleekxmpp.xmlstream import ElementBase


class Query(ElementBase):
    namespace = 'digda:forward'
    name = 'query'
    plugin_attrib = 'dquery'
    interfaces = {'type'}


class Resource(ElementBase):
    namespace = 'digda:forward'
    name = 'resource'
    plugin_attrib = 'dresource'
    interfaces = {'rid', 'transport', 'port'}


class Option(ElementBase):
    namespace = 'digda:forward'
    name = 'option'
    plugin_attrib = 'doption'
    interfaces = {'address', 'baudrate', 'bytesize', 'parity',
                  'stopbits', 'xonxoff', 'rtscts', 'dsrdtr'}


class Destination(ElementBase):
    namespace = 'digda:forward'
    name = 'destination'
    plugin_attrib = 'ddestination'
    interfaces = {'jid'}


class ResourceInfo(ElementBase):
    namespace = 'digda:forward'
    name = 'resource-info'
    plugin_attrib = 'drinfo'
    interfaces = {'info', 'sid', 'rid'}