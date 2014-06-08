# encoding: utf-8
import json
import traceback
import uuid
import time
import zmq
from logging import getLogger
from socket import getfqdn

log = getLogger('emailer.protocol')


class ProtocolException(Exception): pass


class BrokerHandler(object):
    _INSTANCE_ID = {'id': 0}
    WAIT_TIMEOUT = 5

    @classmethod
    def gen_uuid(cls, instance_id):
        return str(uuid.uuid5(uuid.NAMESPACE_OID, "{0}-{1}:{2}".format(str(cls.__name__), getfqdn(), instance_id)))

    def __init__(self, host="localhost", port=5450, handler=lambda x: log.debug(repr(x))):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect ("tcp://{0}:{1}".format(host, port))
        self._INSTANCE_ID['id'] += 1
        self.uuid = self.gen_uuid(self._INSTANCE_ID['id'])
        self.handler = handler

    def _decode_message(self, msg):
        obj = json.loads(msg)
        return obj.get('error'), obj.get('data')

    def _encode_message(self, cmd, data):
        return json.dumps(dict(command=cmd, data=data))

    def send(self, msg):
        self.socket.send(msg)
        error, data = self._decode_message(self.socket.recv())

        if error:
            raise ProtocolException('Broker return error: {0}'.format(unicode(data)))
        else:
            return data

    def store(self, data):
        return self.send(self._encode_message('store', data))

    def get_task(self, wait=True):
        log.debug('Getting task for instance: {0}'.format(self.uuid))
        data = self.send(self._encode_message('assign', self.uuid))
        if data and data.get('id'):
            try:
                log.debug('Got task: {0}'.format(data.get('id')))
                self.handler(data.get('task'))
                self.send(self._encode_message('done', data.get('id')))
                log.debug('Task {0} is done.'.format(data.get('id')))
            except Exception as e:
                log.debug("Error: {0}\n".format(traceback.format_exc()))
                log.error('Task {0} is failed beacuse: {1}'.format(data.get('id'), unicode(e)))
                self.send(self._encode_message('fault', data.get('id')))
        else:
            if wait:
                time.sleep(self.WAIT_TIMEOUT)