#
# Copyright 2013-2014 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from itertools import islice, imap, repeat
import os
import string


class ConstantsHolder(object):

    class ConstantError(TypeError): pass

    def __setattr__(self,name,value):
        if self.__dict__.has_key(name):
            raise self.ConstantError, "Can't rebind constant(%s)"%name
        self.__dict__[name]=value


def random_string(length=5):
    """
    Generates a random string with the size equal to the given length.
    If length is not informed the string size will be 5.
    """
    chars = set(string.ascii_lowercase + string.digits)
    char_gen = (c for c in imap(os.urandom, repeat(1)) if c in chars)
    return ''.join(islice(char_gen, None, length))

