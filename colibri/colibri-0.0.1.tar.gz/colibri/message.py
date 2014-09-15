# -*- coding: utf-8 -*-
from .serialization import (dumps, loads, SHORTSTR, TABLE, OCTET, TIMESTAMP,
                            SHORT, LONGLONG)

__all__ = ['BasicMessage']


def dump_properties(properties, types):
    flags = []
    flag_bits = 0
    shift = 15
    sformat, svalues = [], []
    get_prop = properties.get

    for name, proptype in types:
        value = get_prop(name)
        if value is not None:
            if shift == 0:
                # AMQP allows to have more than one set of properties
                flags.append(flag_bits)
                flag_bits = 0
                shift = 15

            flag_bits |= (1 << shift)
            sformat.append(proptype)
            svalues.append(value)
        shift -= 1
    return flag_bits.to_bytes(2, 'big') + dumps(''.join(sformat), svalues)


def load_properties(raw, types):
    (class_id, weight), offset = loads(SHORT+SHORT, raw)
    assert weight == 0, 'weight must always be 0'
    (body_size, flags), offset = loads(LONGLONG+SHORT, raw, offset=offset)

    flags = bin(flags)[2:]  # strip 0b
    sformat, snames = [], []
    for (name, proptype), flag in zip(types, flags):
        if flag == '1':
            sformat.append(proptype)
            snames.append(name)
    raw_properties, _ = loads(''.join(sformat), raw, offset=offset)
    return body_size, dict(zip(snames, raw_properties))


class BasicMessage(object):

    PROPERTIES = (
        ('content_type', SHORTSTR),
        ('content_encoding', SHORTSTR),
        ('headers', TABLE),
        ('delivery_mode', OCTET),
        ('priority', OCTET),
        ('correlation_id', SHORTSTR),
        ('reply_to', SHORTSTR),
        ('expiration', SHORTSTR),
        ('message_id', SHORTSTR),
        ('timestamp', TIMESTAMP),
        ('type', SHORTSTR),
        ('user_id', SHORTSTR),
        ('app_id', SHORTSTR),
    )

    delivery_info = None

    def __init__(self, body=None, **properties):
        properties.setdefault('content_encoding', 'utf-8')
        if isinstance(body, str):
            body = body.encode(properties['content_encoding'])
        self.body = [] if body is None else body
        self.properties = properties

        # Attributes below are used to create Message object from
        # sequence of frames
        self._body_len = None if body is None else len(body)
        self._body_received = 0
        self._ready = False

    def dump_properties(self, class_id):
        head = dumps('BBL', (class_id, 0, len(self.body)))
        return head + dump_properties(self.properties, self.PROPERTIES)

    def load_properties(self, raw, load_properties=load_properties):
        return load_properties(raw, self.PROPERTIES)

    @property
    def headers(self):
        return self.properties.get('headers')

    @property
    def delivery_tag(self):
        return self.delivery_info.get('delivery_tag')

    # Methods below are used to create Message object from
    # sequence of frames: header -> body [-> body ...]

    def add_header(self, raw):
        self._body_len, self.properties = self.load_properties(raw)
        self.properties.setdefault('content_encoding', 'utf-8')

    def add_body_chunk(self, chunk):
        if self._ready:
            return
        body_len = self._body_len
        assert body_len is not None

        self.body.append(chunk)
        self._body_received += len(chunk)
        assert body_len <= self._body_received, 'Received extra body chunk'

        if body_len == self._body_received:
            self.body = b''.join(self.body)
            self.body = self.body.decode(self.properties['content_encoding'])
            self._ready = True
