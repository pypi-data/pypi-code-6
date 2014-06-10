# Copyright 2013-2014 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Twisted binding for Kazoo.

This doesn't really reimplement Kazoo with Twisted. Instead it delegates
all blocking calls to seperate thread and returns result as Deferred.
This allows usage of using Kazoo in Twisted reactor thread without
blocking it.

"""
from txkazoo._version import __version__
version = __version__

from txkazoo.client import TxKazooClient
from txkazoo.log import TxLogger
from txkazoo.recipe.lock import Lock
from txkazoo.recipe.partitioner import SetPartitioner
__all__ = ("TxKazooClient", "TxLogger", "Lock", "SetPartitioner")
