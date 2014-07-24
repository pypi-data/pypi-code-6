import os
import collections
from hashlib import sha512
from django.contrib.admin.util import NestedObjects
from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.six import add_metaclass
from django.core.urlresolvers import reverse
from django.http import QueryDict

# this is just included to make sure our monkey patches are applied
from .forms import Form
import {{ project_name }}

def get_size(start_path = '.'):
    """http://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

class IterableChoiceEnum(type):
    def __iter__(self):
        """Simply return the iterator of the _choices tuple"""
        return iter(self._choices)

@add_metaclass(IterableChoiceEnum)
class ChoiceEnum(object):
    """
    This creates an iterable *class* (as opposed to an iterable *instance* of a
    class). Subclasses must define a class variable called `_choices` which is a
    list of 2-tuples. Subclasses can be passed directly to a field as the
    `choice` kwarg.

    For example:

    class FooType(ChoiceEnum):
    A = 1
    B = 2

    _choices = (
    (A, "Alpha"),
    (B, "Beta"),
    )


    class SomeModel(models.Model):
    foo = models.ChoiceField(choices=FooType)
    """
    _choices = ()
    # http://stackoverflow.com/questions/5434400/python-is-it-possible-to-make-a-class-iterable-using-the-standard-syntax

# stolen from werkzeug.http
def parse_range_header(value):
    """Parses a range header into a :class:`~werkzeug.datastructures.Range`
    object.  If the header is missing or malformed `None` is returned.
    `ranges` is a list of ``(start, stop)`` tuples where the ranges are
    non-inclusive.

    .. versionadded:: 0.7
    """
    if not value or '=' not in value:
        return None

    ranges = []
    last_end = 0
    units, rng = value.split('=', 1)
    units = units.strip().lower()

    for item in rng.split(','):
        item = item.strip()
        if '-' not in item:
            return None
        if item.startswith('-'):
            if last_end < 0:
                return None
            begin = int(item)
            end = None
            last_end = -1
        elif '-' in item:
            begin, end = item.split('-', 1)
            begin = int(begin)
            if begin < last_end or last_end < 0:
                return None
            if end:
                end = int(end) + 1
                if begin >= end:
                    return None
            else:
                end = None
            last_end = end
        ranges.append((begin, end))

    return units, ranges


def will_be_deleted_with(obj):
    """
    Pass in any Django model object that you intend to delete.
    This will iterate over all the model classes that would be affected by the
    deletion, yielding a two-tuple: the model class, and a set of all the objects of
    that type that would be deleted.

    This ignores any models that are not in the `vcp` package.
    """
    collector = NestedObjects(using="default")
    collector.collect([obj])
    # the collector returns a list of all objects in the database that
    # would be deleted if `obj` were deleted.
    for cls, list_of_items_to_be_deleted in collector.data.items():
        # ignore any classes that aren't in the vcp package
        if not cls.__module__.startswith(vcp.__name__):
            continue

        # remove obj itself from the list
        if cls == obj.__class__:
            list_of_items_to_be_deleted = set(item for item in list_of_items_to_be_deleted if item.pk != obj.pk)
            if len(list_of_items_to_be_deleted) == 0:
                continue

        yield cls, list_of_items_to_be_deleted

def build_url(*args, **kwargs):
    params = kwargs.pop('params', {})
    url = reverse(*args, **kwargs)
    if not params: return url

    qdict = QueryDict('', mutable=True)
    for k, v in params.iteritems():
        if type(v) is list: qdict.setlist(k, v)
        else: qdict[k] = v

    return url + '?' + qdict.urlencode()



class DrupalPasswordHasher(BasePasswordHasher):
    '''
    Hashes a Drupal 7 password with the prefix 'drupal'
    Used for legacy passwords from VCP 2.0.

    snippet from https://djangosnippets.org/snippets/2729/#c4520
    modified for compatibility with Django 1.6

    '''

    algorithm = "drupal"
    iter_code = 'C'
    salt_length = 8

    def encode(self, password, salt, iter_code=None):
        """The Drupal 7 method of encoding passwords"""

        _ITOA64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

        if iter_code == None:
            iterations = 2 ** _ITOA64.index(self.iter_code)
        else:
            iterations = 2 ** _ITOA64.index(iter_code)

        # convert these to bytestrings to get rid of dumb decoding errors:
        salt = str(salt)
        password = str(password)

        hashed_string = sha512(salt + password).digest()

        for i in range(iterations):    
            hashed_string = sha512(hashed_string + password).digest()


        l = len(hashed_string)

        output = ''
        i = 0

        while i < l:
            value = ord(hashed_string[i])
            i = i + 1

            output += _ITOA64[value & 0x3f]
            if i < l:
                value |= ord(hashed_string[i]) << 8

            output += _ITOA64[(value >> 6) & 0x3f]
            if i >= l:
                break
            i += 1

            if i < l:
                value |= ord(hashed_string[i]) << 16

            output += _ITOA64[(value >> 12) & 0x3f]
            if i >= l:
                break
            i += 1

            output += _ITOA64[(value >> 18) & 0x3f]

        long_hashed = "%s$%s%s%s" % (self.algorithm, iter_code,
                salt, output)
        return long_hashed[:59]


    def verify(self, password, encoded):
        hash = encoded.split("$")[1]
        iter_code = hash[0]
        salt = hash[1:1 + self.salt_length]        
        test_encoded = self.encode(password, salt, iter_code)
        return encoded == test_encoded
