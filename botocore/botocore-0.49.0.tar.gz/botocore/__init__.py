# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
# Copyright 2012-2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import os
import re
import logging

__version__ = '0.49.0'


class NullHandler(logging.Handler):
    def emit(self, record):
        pass

# Configure default logger to do nothing
log = logging.getLogger('botocore')
log.addHandler(NullHandler())


_first_cap_regex = re.compile('(.)([A-Z][a-z]+)')
_number_cap_regex = re.compile('([a-z])([0-9]+)')
_end_cap_regex = re.compile('([a-z0-9])([A-Z])')
# Prepopulate the cache with special cases that don't match
# our regular transformation.
_xform_cache = {
    ('SwapEnvironmentCNAMEs', '_'): 'swap_environment_cnames',
    ('SwapEnvironmentCNAMEs', '-'): 'swap-environment-cnames',
    ('CreateCachediSCSIVolume', '_'): 'create_cached_iscsi_volume',
    ('CreateCachediSCSIVolume', '-'): 'create-cached-iscsi-volume',
    ('DescribeCachediSCSIVolumes', '_'): 'describe_cached_iscsi_volumes',
    ('DescribeCachediSCSIVolumes', '-'): 'describe-cached-iscsi-volumes',
    ('DescribeStorediSCSIVolumes', '_'): 'describe_stored_iscsi_volumes',
    ('DescribeStorediSCSIVolumes', '-'): 'describe-stored-iscsi-volumes',
    ('CreateStorediSCSIVolume', '_'): 'create_stored_iscsi_volume',
    ('CreateStorediSCSIVolume', '-'): 'create-stored-iscsi-volume',
    ('NotificationARNs', '_'): 'notification_arns',
    ('NotificationARNs', '-'): 'notification-arns',
}
ScalarTypes = ('string', 'integer', 'boolean', 'timestamp', 'float', 'double')

BOTOCORE_ROOT = os.path.dirname(os.path.abspath(__file__))


def xform_name(name, sep='_', _xform_cache=_xform_cache):
    """Convert camel case to a "pythonic" name.

    If the name contains the ``sep`` character, then it is
    returned unchanged.

    """
    if sep in name:
        # If the sep is in the name, assume that it's already
        # transformed and return the string unchanged.
        return name
    key = (name, sep)
    if key not in _xform_cache:
        s1 = _first_cap_regex.sub(r'\1' + sep + r'\2', name)
        s2 = _number_cap_regex.sub(r'\1' + sep + r'\2', s1)
        transformed = _end_cap_regex.sub(r'\1' + sep + r'\2', s2).lower()
        _xform_cache[key] = transformed
    return _xform_cache[key]


class BotoCoreObject(object):

    def __init__(self, **kwargs):
        self.name = ''
        self.py_name = None
        self.cli_name = None
        self.type = None
        self.members = []
        self.documentation = ''
        self.__dict__.update(kwargs)
        if self.py_name is None:
            self.py_name = xform_name(self.name, '_')
        if self.cli_name is None:
            self.cli_name = xform_name(self.name, '-')

    def __repr__(self):
        return '%s:%s' % (self.type, self.name)
