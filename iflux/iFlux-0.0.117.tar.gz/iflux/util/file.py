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
import os


def write(path, data):
    """
    Writes a given data to a file located at the given path.
    """
    with open(path, 'w') as f:
        f.write(data)
    f.close()


def read(path):
    """
    Reads a file located at the given path.
    """
    data = None
    with open(path, 'r') as f:
        data = f.read()
    f.close()
    return data


def touch(path):
    """
    Creates a file located at the given path.
    """
    with open(path, 'a') as f:
        os.utime(path, None)
    f.close()
