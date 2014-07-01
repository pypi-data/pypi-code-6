#!/usr/bin/env python
# -*- coding: utf-8  -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2012 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
#  more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

"""
File Monitor Utilities
"""


def raise_exception(path, message=u"Fake error for testing"):
    """
    File monitor action which always raises an exception.

    This is meant to be a simple way to test the error handling of a file
    monitor.  For example, whether or not file processing continues for
    subsequent files after the first error is encountered.  If logging
    configuration dictates that an email should be sent, it will of course test
    that as well.
    """
    raise Exception(u'{0}: {1}'.format(message, path))
