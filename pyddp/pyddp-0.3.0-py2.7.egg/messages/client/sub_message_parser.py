# -*- coding: utf-8 -*-

# Copyright 2014 Foxdog Studios
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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .client_message_parser import ClientMessageParser
from .constants import MSG_SUB
from .sub_message import SubMessage

__all__ = ['SubMessageParser']


class SubMessageParser(ClientMessageParser):
    MESSAGE_TYPE = MSG_SUB

    def parse(self, pod):
        return SubMessage(pod['id'], pod['name'], params=pod.get('params'))

