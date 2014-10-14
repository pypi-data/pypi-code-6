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

import iflux
import iflux.conf
import iflux.core.handlers
import tornado


class ApplicationInfoHandler(iflux.core.handlers.RequestHandler):
    def get(self):
        self.render('info.html',
            tornado_version=tornado.version,
            iflux=iflux,
            iflux_conf=iflux.conf,
            handlers=self.application.handlers[0][1])
