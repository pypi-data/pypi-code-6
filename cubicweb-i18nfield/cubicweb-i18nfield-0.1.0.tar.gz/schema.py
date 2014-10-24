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

"""cubicweb-i18nfield schema"""


from yams.buildobjs import (EntityType, RelationType, RelationDefinition,
                            String, Datetime, SubjectRelation)

from cubicweb.schema import RQLConstraint


class I18nLang(EntityType):
    """Partly taken from i18ncontent ; note this makes current cube
    and i18ncontent incompatible.

    registered language for an application.

    See http://www.loc.gov/standards/iso639-2 for available codes.
    """
    code = String(required=True, maxsize=2, unique=True,
                  description=_('ISO 639.2 Code'))
    name = String(required=True, internationalizable=True, maxsize=37,
                  description=_('ISO description'))


class I18nField(EntityType):
    __unique_together__ = [('field_name', 'i18nfield_of')]
    __permissions__ = {'read': ('managers', 'users', 'guests',),
                       'add': (),
                       'update': (),
                       'delete': ()}
    field_name = String(required=True, maxsize=64)
    last_edited = Datetime(required=True, default='NOW')


other_lang_cstr = RQLConstraint('S of_field F, F i18nfield_of E, E ref_lang L, '
                                'NOT O identity L')

class Translation(EntityType):
    __unique_together__ = [('lang', 'of_field')]
    value = String()
    lang = SubjectRelation('I18nLang', cardinality='1*', inlined=True,
                           constraints=[other_lang_cstr])
    of_field = SubjectRelation('I18nField', cardinality='1*', inlined=True,
                               composite='object')


STRICTLY_AUTO_REL_PERMS = {'read': ('managers', 'users', 'guests',),
                           'add': (),
                           'delete': ()}


class ref_lang(RelationType):
    object = 'I18nLang'
    cardinality = '1*'
    inlined = True


class i18nfield_of(RelationType):
    __permissions__ = STRICTLY_AUTO_REL_PERMS
    subject = 'I18nField'
    cardinality = '1*'
    inlined = True
    composite = 'object'
