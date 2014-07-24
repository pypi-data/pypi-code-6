# -*- coding: utf-8 -*-

# Copyright 2014 Rémi Duraffort
# This file is part of SMSForward.
#
# SMSForward is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SMSForward is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SMSForward.  If not, see <http://www.gnu.org/licenses/>.

from . import provider

import requests


class MobileFreeFr(provider.Provider):
    def __init__(self, cfg):
        self.user = cfg['user']
        self.token = cfg['token']

    def send_message(self, message):
        params = {'user': self.user,
                  'pass': self.token,
                  'msg': message}
        response = requests.get("https://smsapi.free-mobile.fr/sendmsg", params=params, verify=False)
        return response
