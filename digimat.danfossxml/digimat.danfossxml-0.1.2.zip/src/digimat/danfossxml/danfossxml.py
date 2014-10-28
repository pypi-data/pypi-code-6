import xml.etree.ElementTree as ET
import csv
import sys, logging, logging.handlers
import time

# pip install unidecode
from unidecode import unidecode

# pip install requests
import requests


class DanfossItem(object):
    def __init__(self, device, cid, vid, unit='', tag=''):
        self._key = DanfossItem.computeKey(cid, vid)
        self._device = device
        self._cid = int(cid)
        self._vid = int(vid)
        self._tag = tag
        self._value = 0
        self._unit = unit
        self._stamp=0
        self._uuid = DanfossItem.computeUUID(
            device.nodetype, device.node, cid, vid)

    @property
    def device(self):
        return self._device

    @property
    def interface(self):
        return self.device.interface

    @property
    def logger(self):
        return self.interface.logger

    @staticmethod
    def computeKey(cid, vid):
        return '%d/%d' % (int(cid), int(vid))

    @staticmethod
    def computeUUID(nodetype, node, cid, vid):
        return '%d/%d/%d/%d' % (int(nodetype), int(node), int(cid), int(vid))

    @property
    def key(self):
        return self._key

    @property
    def uuid(self):
        return self._uuid

    @property
    def cid(self):
        return self._cid

    @property
    def vid(self):
        return self._vid

    @property
    def tag(self):
        return self._tag

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            self._value = float(value)
            self._stamp=time.time()
        except:
            pass

    @property
    def unit(self):
        return self._unit

    def age(self):
        return time.time()-self._stamp

    def __str__(self):
        return 'did=%s:node=%d/%d:cid=%d:vid=%d:tag=%s:value=%.02f %s' % (self.device.did,
            self.device.nodetype, self.device.node,
            self.cid, self.vid, self.tag,
            self.value, self.unit)

    def dump(self):
        print str(self)

    def manager(self):
        pass

    def read(self):
        self.device.interface.readItems([self])


class DanfossItems(object):
    def __init__(self, device):
        self._device = device
        self._items = {}

    @property
    def device(self):
        return self._device

    @property
    def interface(self):
        return self.device.interface

    @property
    def logger(self):
        return self.interface.logger

    def get(self, key):
        try:
            return self._items[key]
        except:
            pass

    def __getitem__(self, key):
        return self.get(key)

    def add(self, cid, vid, unit='', tag=''):
        item = self.get(DanfossItem.computeKey(cid, vid))
        if not item:
            item = DanfossItem(self.device, cid, vid, unit, tag)
            self._items[item.key] = item
            self.logger.info('device(%s).items.add(%s)' % (self.device.key, item.key))
        return item

    def __iter__(self):
        return self._items.values().__iter__()

    def manager(self):
        for item in self._items.values():
            item.manager()

    def dump(self):
        for item in self.items:
            item.dump()


class DanfossDevice(object):
    def __init__(self, interface, did, nodetype, node, tag=''):
        self._interface = interface
        self._items = DanfossItems(self)
        self._key = DanfossDevice.computeKey(nodetype, node)
        self._did = did
        #self._dtype = dtype
        self._nodetype = int(nodetype)
        self._node = int(node)
        try:
            self._tag = str(tag)
        except:
            self._tag = '???'

    @staticmethod
    def computeKey(nodetype, node):
        return '%d/%d' % (int(nodetype), int(node))

    @property
    def items(self):
        return self._items

    @property
    def interface(self):
        return self._interface

    @property
    def logger(self):
        return self.interface.logger

    @property
    def did(self):
        return self._did

    @property
    def nodetype(self):
        return self._nodetype

    @property
    def node(self):
        return self._node

    # @property
    # def dtype(self):
    #     return self._dtype

    @property
    def key(self):
        return self._key

    @property
    def tag(self):
        return self._tag

    def __str__(self):
        return 'device[did=%s:node=%d/%d:tag=%s]' % (self.did, self.nodetype, self.node, self.tag)

    def dump(self):
        self._items.dump()

    def manager(self):
        self._items.manager()

    def read(self):
        self.interface.readItems(self.items)


class DanfossDevices(object):
    def __init__(self, interface):
        self._interface = interface
        self._devices = {}

    @property
    def interface(self):
        return self._interface

    @property
    def logger(self):
        return self.interface.logger

    def get(self, key):
        try:
            return self._devices[key]
        except:
            pass

    def __getitem__(self, key):
        return self.get(key)

    def add(self, did, nodetype, node, tag=''):
        device = self.get(DanfossDevice.computeKey(nodetype, node))
        if not device:
            device = DanfossDevice(
                self.interface, did, nodetype, node, tag)
            self._devices[device.key] = device
            self.logger.info("devices.add(%s)" % device.key)
        return device

    def __iter__(self):
        return self._devices.values().__iter__()

    def dump(self):
        for device in self.devices():
            device.dump()

    def manager(self):
        for device in self._devices.value():
            device.manager()


class DanfossXML(object):
    def __init__(self, host, logger=None):
        if not logger:
            logger=logging.getLogger("DanfossXML(%s)" % host)
            logger.setLevel(logging.DEBUG)
            ch = logging.StreamHandler(sys.stdout)
            ch.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s:%(name)s::%(levelname)s::%(message)s')
            ch.setFormatter(formatter)
            logger.addHandler(ch)

        self._logger=logger
        self._host = host
        self._url = 'http://'
        self._params = {
            'lang': 'e', 'units': 's', 'date_format': '2', 'time_format': '1'}
        # if not compress:
        #     self._params['compress'] = '0'
        self._devices = DanfossDevices(self)
        self._cache_discoverDeviceItems={}

    @property
    def devices(self):
        return self._devices

    @property
    def logger(self):
        return self._logger

    def url(self):
        return 'http://%s/html/xml.cgi' % self._host

    def request(self, xmlCommand):
        data = ET.tostring(xmlCommand)
        self.logger.debug('request(%s)' % ((data[:60] + '...') if len(data) > 60 else data))
        r = requests.post(self.url(), data=data, timeout=20.0)
        if r.status_code == 200:
            try:
                return ET.fromstring(r.content)
            except:
                pass

    def buildXmlCommand(self, name, params={}):
        try:
            root = ET.fromstring("<cmd action='%s'/>" % name)
            for p in self._params.items():
                root.set(p[0], p[1])
            for p in params.items():
                root.set(p[0], p[1])
            return root
        except:
            pass

    def read_devices(self):
        return self.request(self.buildXmlCommand('read_devices'))

    def read_parm_info(self, did):
        params = {'device_id': did}
        return self.request(self.buildXmlCommand('read_parm_info', params))

    def read_val(self, items):
        params = {'num_only': '1'}
        xcmd = self.buildXmlCommand('read_val', params)
        index = {}
        for item in items:
            try:
                index[item.uuid] = item
                xread = ET.SubElement(xcmd, 'val')
                xread.set('nodetype', str(item.device.nodetype))
                xread.set('node', str(item.device.node))
                xread.set('cid', str(item.cid))
                xread.set('vid', str(item.vid))
            except:
                pass

        xresp = self.request(xcmd)
        for xval in xresp.findall('./val'):
            try:
                nodetype = xval.get('nodetype')
                node = xval.get('node')
                cid = xval.get('cid')
                vid = xval.get('vid')
                value = xval.get('parval')
                uuid = DanfossItem.computeUUID(nodetype, node, cid, vid)
                item = index[uuid]
                item.value = value
            except:
                self.logger.error('read_val()')

    def discoverDevices(self):
        xresp = self.read_devices()
        for xdevice in xresp.findall('./device'):
            try:
                #print ET.dump(xdevice)
                did = xdevice.find('device_id').text
                #dtype = xdevice.find('type').text
                tag = xdevice.find('name').text
                try:
                    tag=unidecode(unicode(tag))
                except:
                    pass
                tag = tag.strip(' ')

                nodetype = xdevice.get('nodetype')
                node = xdevice.get('node')
                #print did, nodetype, node, tag
                self.devices.add(did, nodetype, node, tag)
            except:
                pass

    def discoverDeviceItems(self, device):
        xresp=None
        try:
            xresp=self._cache_discoverDeviceItems[device.did]
        except:
            pass

        if xresp is None:
            xresp = self.read_parm_info(device.did)
            self._cache_discoverDeviceItems[device.did]=xresp

        if xresp is not None:
            for xitem in xresp.findall('./parms/parm'):
                try:
                    #print ET.dump(xitem)
                    cid = xitem.get('cid')
                    vid = xitem.get('vid')
                    unit = xitem.get('unit')
                    tag = xitem.get('name')
                    try:
                        tag=unidecode(unicode(tag))
                    except:
                        pass
                    #tag=tag.replace('---', '')
                    tag = tag.strip(' ')
                    device.items.add(cid, vid, unit, tag)
                except:
                    pass

    def discover(self):
        self.discoverDevices()
        for device in self.devices:
            self.discoverDeviceItems(device)

    def readItems(self, items):
        self.read_val(items)

    def read(self):
        for device in self.devices:
            device.read()

    def csv(self, filepath, discover=False):
        if discover:
            self.discover()
            self.read()

        with open(filepath, 'wb') as f:
            writer = csv.writer(f, dialect='excel', quotechar='"',
                                quoting=csv.QUOTE_ALL, delimiter=';')

            headers = ('digimat_id', 'danfoss_device_id', 'danfoss_device_label', 'danfoss_node_type',
                       'danfoss_node', 'danfoss_component_id (cid)',
                       'danfoss_variable_id (vid)', 'danfoss_label',
                       'scanned_value', 'scanned_unit')
            writer.writerow(headers)

            index = 0
            for device in self.devices:
                for item in device.items:
                    row = (index, device.did, device.tag, device.nodetype,
                           device.node, item.cid, item.vid,
                           item.tag, item.value, item.unit)
                    writer.writerow(row)
                    index += 1

    def dump(self):
        for device in self.devices:
            for item in device.items:
                item.dump()


if __name__ == '__main__':
    pass

