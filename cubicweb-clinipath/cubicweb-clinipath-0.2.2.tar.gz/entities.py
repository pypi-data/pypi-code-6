# -*- coding: utf-8 -*-
# copyright 2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
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

"""cubicweb-clinipath entity's classes"""

from cubicweb.entities import AnyEntity


class Biopsy(AnyEntity):
    __regid__ = 'Biopsy'

    def dc_title(self):
        return u'%s (%s)' % (self._cw._('Biopsy'), self.reverse_related_samples[0].dc_title())


class BiopsySample(AnyEntity):
    __regid__ = 'BiopsySample'

    def dc_title(self):
        return u'%s (%s)' % (self._cw._('BiopsySample'), self.extracted_from[0].dc_title())


class AnatomicPathologyReport(AnyEntity):
    __regid__ = 'AnatomicPathologyReport'

    def dc_title(self):
        return u'%s (%s)' % (self._cw._('AnatomicPathologyReport'), self.report_on[0].dc_title())

    @property
    def formatted_content(self):
        return u'\n'.join([d for d in (self.description, self.conclusions) if d])
