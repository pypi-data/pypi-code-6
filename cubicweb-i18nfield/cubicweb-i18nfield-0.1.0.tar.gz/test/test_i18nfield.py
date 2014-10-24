# -*- coding: utf-8 -*-
# copyright 2011 Florent Cayré (Villejuif, FRANCE), all rights reserved.
# contact http://www.cubicweb.org/project/cubicweb-i18nfield
# mailto:Florent Cayré <florent.cayre@gmail.com>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-i18nfield automatic tests"""

from cubicweb.devtools.testlib import AutomaticWebTest

class AutomaticWebTest(AutomaticWebTest):
    '''provides `to_test_etypes` and/or `list_startup_views` implementation
    to limit test scope
    '''

    def setup_database(self):
        req = self.request()
        req.create_entity('I18nLang', code=u'en', name=u'English')
        self.commit()

    def test_ten_each_config(self):
        # Would need more config
        pass


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
