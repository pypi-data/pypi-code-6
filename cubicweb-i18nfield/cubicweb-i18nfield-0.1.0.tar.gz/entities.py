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

"""cubicweb-i18nfield entity's classes"""

from logilab.common.decorators import cached

from cubicweb.entity import _marker
from cubicweb.entities import AnyEntity, fetch_config
from cubicweb.view import EntityAdapter


def target_lang_code(req):
    # warning, req can be a server session (with no 'form' attr)
    return req.data.setdefault(
        'i18nfield_target_lang',
        getattr(req, 'form', {}).get('lang_code', req.lang))


class I18nLang(AnyEntity):
    __regid__ = 'I18nLang'
    fetch_attrs, cw_fetch_order = fetch_config(['code'])


class I18nField(AnyEntity):
    __regid__ = 'I18nField'
    fetch_attrs, cw_fetch_order = fetch_config(['field_name'])

    def original_value(self):
        return getattr(self.i18nfield_of[0], self.field_name)

    def translation(self, lang_code):
        rql = ('Any T,L,V WHERE T lang L, T value V, L code %(l)s, '
               'T of_field F, F eid %(f)s')
        rset = self._cw.execute(rql, {'l': lang_code, 'f': self.eid})
        if rset:
            return rset.get_entity(0, 0)
        else:
            return None


class Translation(AnyEntity):
    __regid__ = 'Translation'

    def is_outdated(self):
        return self.modification_date < self.of_field[0].last_edited


class _TranslatableEntityAdapter(EntityAdapter):
    __regid__ = 'translatable_entity'

    @property
    def ref_code(self):
        return self.entity.ref_lang[0].code

    @cached
    def i18nfield(self, attr):
        ctx = {'e': self.entity.eid, 'f': attr}
        rql = ('Any F,N,D '
               'WHERE F is I18nField, F field_name N, F last_edited D, '
               'F i18nfield_of E, E eid %(e)s, F field_name %(f)s')
        rset = self._cw.execute(rql, ctx)
        return rset.rowcount and rset.get_entity(0, 0) or None

    @cached
    def translation(self, attr, lang_code=None):
        lang_code = lang_code or self._cw.lang
        ctx = {'l': lang_code, 'f': attr, 'e': self.entity.eid}
        rset = self._cw.execute('Any T WHERE T is Translation, '
                                'T value V, T modification_date TMD, '
                                'T lang L, L code %(l)s, T of_field F, '
                                'F field_name %(f)s, F last_edited FMD, '
                                'F i18nfield_of E, E eid %(e)s', ctx)
        return rset.get_entity(0, 0) if rset.rowcount else None


    @cached
    def translated_attr(self, attr, lang_code):
        ctx = {'l': lang_code, 'f': attr, 'e': self.entity.eid}
        rset = self._cw.execute('Any V,TMD,FMD WHERE T is Translation, '
                                'T value V, T modification_date TMD, '
                                'T lang L, L code %(l)s, T of_field F, '
                                'F field_name %(f)s, F last_edited FMD, '
                                'F i18nfield_of E, E eid %(e)s', ctx)
        if rset.rowcount:
            value, tdate, fdate = rset[0]
            if tdate < fdate:
                self.warning('Could not find up-to-date %s translation for '
                             'field %s of entity %s; returning version of %s',
                             lang_code, attr, self.entity.eid, tdate)
        else:
            self.warning('Could not find %s translation for field %s '
                         'of entity %s', lang_code, attr, self.entity.eid)
            value = getattr(self.entity, attr)
        return value

    def translation_infos(self):
        '''for each language defined in the system, returns infos about current
        entity translations in a (lang, infos) list, where infos holds
        Translation and I18nField instances if a translation exists, and
        None otherwise.
        '''
        all_langs = self._cw.execute('Any L,C,N WHERE L is I18nLang, '
                                     'L code C, L name N').entities(0)
        rql = ('Any L,T,TD,F,FN,FD WHERE L is I18nLang, T lang L, '
               'T modification_date TD, T of_field F, F last_edited FD, '
               'F field_name FN, F i18nfield_of E, E eid %(e)s')
        rset = self._cw.execute(rql, {'e': self.entity.eid})
        infos = {}
        for i, row in enumerate(rset.rows):
            translation, field = rset.get_entity(i, 1), rset.get_entity(i, 3)
            infos.setdefault(row[0], []).append((translation, field))
        return [(lang, infos.get(lang.eid)) for lang in all_langs
                if lang.eid != self.entity.ref_lang[0].eid]


class TranslatableEntityMixin(object):
    i18nfields = ()

    def printable_value(self, attr, value=_marker, attrtype=None,
                        format='text/html', displaytime=True):
        uattr = unicode(attr) # attr could be a rschema object
        if uattr in self.i18nfields and value == _marker:
            adapted = self.cw_adapt_to('translatable_entity')
            tlang_code = target_lang_code(self._cw)
            if adapted.ref_code != tlang_code:
                value = adapted.translated_attr(uattr, tlang_code)
        return super(TranslatableEntityMixin, self).printable_value(
            attr, value, attrtype, format)
