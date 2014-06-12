# -*- coding: utf-8 -*-
'''
    vdirsyncer.utils.vobject
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 Markus Unterwaditzer & contributors
    :license: MIT, see LICENSE for more details.
'''
import hashlib

import icalendar.cal
import icalendar.parser
import icalendar.caselessdict

from . import cached_property
from .compat import text_type, itervalues


def _process_properties(*s):
    rv = set()
    for key in s:
        rv.add(key + ':')
        rv.add(key + ';')

    return tuple(rv)


IGNORE_PROPS = _process_properties(
    # PRODID is changed by radicale for some reason after upload
    'PRODID',
    # VERSION can get lost in singlefile storage
    'VERSION',
    # X-RADICALE-NAME is used by radicale, because hrefs don't really exist in
    # their filesystem backend
    'X-RADICALE-NAME',
    # REV is from the VCARD specification and is supposed to change when the
    # item does -- however, we can determine that ourselves
    'REV'
)

# Whether the installed icalendar version has
# https://github.com/collective/icalendar/pull/136
# (support for keeping the order of properties and parameters)
#
# This basically checks whether the superclass of all icalendar classes has a
# method from OrderedDict.
ICALENDAR_ORIGINAL_ORDER_SUPPORT = \
    hasattr(icalendar.caselessdict.CaselessDict, '__reversed__')


class Item(object):

    '''should-be-immutable wrapper class for VCALENDAR (VEVENT, VTODO) and
    VCARD'''

    def __init__(self, raw):
        assert isinstance(raw, text_type)

        self._raw = raw

    @cached_property
    def raw(self):
        '''Raw content of the item, which vdirsyncer doesn't validate in any
        way.'''
        return self._raw

    @cached_property
    def uid(self):
        '''Global identifier of the item, across storages, doesn't change after
        a modification of the item.'''
        stack = [self.parsed]
        while stack:
            component = stack.pop()
            if component is None:
                continue
            uid = component.get('UID', None)
            if uid:
                return uid
            stack.extend(component.subcomponents)

        for line in self.raw.splitlines():
            if line.startswith(u'UID:'):
                uid = line[4:].strip()
                if uid:
                    return uid

    @cached_property
    def hash(self):
        '''Hash of self.raw, used for etags.'''
        return hash_item(self.raw)

    @cached_property
    def ident(self):
        '''Used for generating hrefs and matching up items during
        synchronization. This is either the UID or the hash of the item's
        content.'''
        return self.uid or self.hash

    @cached_property
    def parsed(self):
        try:
            return icalendar.cal.Component.from_ical(self.raw)
        except Exception:
            return None


def normalize_item(item, ignore_props=IGNORE_PROPS, use_icalendar=True):
    if not isinstance(item, Item):
        item = Item(item)
    if use_icalendar and item.parsed is not None:
        # We have to explicitly check "is not None" here because VCALENDARS
        # with only subcomponents and no own properties are also false-ish.
        lines = to_unicode_lines(item.parsed)
    else:
        lines = sorted(item.raw.splitlines())

    return u'\r\n'.join(line.strip()
                        for line in lines
                        if line.strip() and
                        not line.startswith(IGNORE_PROPS))


def hash_item(text):
    return hashlib.sha256(normalize_item(text).encode('utf-8')).hexdigest()


def split_collection(text, inline=(u'VTIMEZONE',),
                     wrap_items_with=(u'VCALENDAR',)):
    '''Emits items in the order they occur in the text.'''
    assert isinstance(text, text_type)
    collection = icalendar.cal.Component.from_ical(text)
    items = collection.subcomponents

    if collection.name in wrap_items_with:
        start = u'BEGIN:{}'.format(collection.name)
        end = u'END:{}'.format(collection.name)
    else:
        start = end = u''

    inlined_items = {}
    for item in items:
        if item.name in inline:
            inlined_items[item.name] = item

    for item in items:
        if item.name not in inline:
            lines = []
            lines.append(start)
            for inlined_item in itervalues(inlined_items):
                lines.extend(to_unicode_lines(inlined_item))

            lines.extend(to_unicode_lines(item))
            lines.append(end)

            yield u''.join(line + u'\r\n' for line in lines if line)


def to_unicode_lines(item):
    '''icalendar doesn't provide an efficient way of getting the ical data as
    unicode. So let's do it ourselves.'''

    if ICALENDAR_ORIGINAL_ORDER_SUPPORT:
        content_lines = item.content_lines(sorted=False)
    else:
        content_lines = item.content_lines()

    for content_line in content_lines:
        if content_line:
            # https://github.com/untitaker/vdirsyncer/issues/70
            # icalendar escapes semicolons which are not supposed to get
            # escaped, because it is not aware of vcard
            content_line = content_line.replace(u'\\;', u';')
            yield icalendar.parser.foldline(content_line)


def join_collection(items, wrappers={
    u'VCALENDAR': (u'VCALENDAR', (u'VTIMEZONE',)),
    u'VCARD': (u'VADDRESSBOOK', ())
}):
    '''
    :param wrappers: {
        item_type: wrapper_type, items_to_inline
    }
    '''
    inline = {}
    components = []
    wrapper_type = None
    inline_types = None
    item_type = None

    def handle_item(item):
        if item.name in inline_types:
            inline[item.name] = item
        else:
            components.append(item)

    for item in items:
        component = icalendar.cal.Component.from_ical(item)

        if item_type is None:
            item_type = component.name
            wrapper_type, inline_types = wrappers[item_type]

        if component.name == item_type:
            if item_type == wrapper_type:
                for subcomponent in component.subcomponents:
                    handle_item(subcomponent)
            else:
                handle_item(component)

    start = end = u''
    if wrapper_type is not None:
        start = u'BEGIN:{}'.format(wrapper_type)
        end = u'END:{}'.format(wrapper_type)

    lines = [start]
    for inlined_item in itervalues(inline):
        lines.extend(to_unicode_lines(inlined_item))
    for component in components:
        lines.extend(to_unicode_lines(component))
    lines.append(end)

    return u''.join(line + u'\r\n' for line in lines if line)
