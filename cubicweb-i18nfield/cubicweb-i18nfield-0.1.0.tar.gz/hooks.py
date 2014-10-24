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

"""cubicweb-i18nfield specific hooks and operations"""

from cubicweb.selectors import adaptable, is_instance
from cubicweb.server.hook import Hook, DataOperationMixIn, Operation, match_rtype

from cubes.i18nfield.utils import set_lang, remove_lang


# translatable entities related classes

class TranslatableEntityAddHook(Hook):
    __regid__ = 'i18nfield.translatable_entity_add'
    __select__ = Hook.__select__ & adaptable('translatable_entity')
    events = ('after_add_entity',)

    def __call__(self):
        langs = self._cw.get_shared_data('i18nfield_lang', {})
        for field in self.entity.i18nfields:
            lang = langs.get(field, u'en')
            ctx = {'e': self.entity.eid, 'c': lang, 'f': field}
            rql = 'Any L WHERE L is I18nLang, L code %(c)s'
            rset = self._cw.execute(rql, ctx)
            if rset.rowcount == 0:
                raise ValueError, self._cw._('language "%s" not found') % lang
            elang = rset.get_entity(0, 0)
            self._cw.create_entity('I18nField', field_name=field,
                                   i18nfield_of=self.entity)


class TranslatableEntityUpdateHook(Hook):
    """
    @test_translatable_entity_udpate
    """
    __regid__ = 'i18nfield.translatable_entity_udpate'
    __select__ = Hook.__select__ & adaptable('translatable_entity')
    events = ('before_update_entity',)
    query = ('SET F last_edited NOW WHERE F is I18nField, '
             'F field_name IN (%s), F i18nfield_of X, '
             'X eid %%(x)s')

    def __call__(self):
        attrs = set(self.entity.i18nfields).intersection(self.entity.cw_edited)
        if attrs:
            field_names = ','.join("'%s'" % a for a in attrs)
            query = self.query % field_names
            self._cw.execute(query % {'x': self.entity.eid})



# lang cache update related classes

class LangCacheUpdateMixin(object):

    def lang_dict(self, lang):
        lang.complete()
        lang_dict = lang.cw_attr_cache.copy()
        del lang_dict['cwuri']
        lang_dict['eid'] = lang.eid
        return lang_dict

    def update_cache(self, lang, op):
        if op == 'remove':
            remove_lang(lang.eid)
        elif op == 'set':
            set_lang(lang.eid, self.lang_dict(lang))


class UpdateLangCacheOp(LangCacheUpdateMixin, DataOperationMixIn, Operation):

    def precommit_event(self):
        for (lang, op) in self.get_data():
            self.update_cache(lang, op)


class AddUpdateI18nLangHook(Hook):
    __regid__ = 'i18nfield.add_update_lang'
    __select__ = Hook.__select__ & is_instance('I18nLang')
    events = ('after_update_entity', 'after_add_entity')

    def __call__(self):
        UpdateLangCacheOp.get_instance(self._cw).add_data((self.entity, 'set'))


class RemoveI18nLangHook(Hook):
    __regid__ = 'i18nfield.remove_lang'
    __select__ = Hook.__select__ & is_instance('I18nLang')
    events = ('after_delete_entity',)

    def __call__(self):
        UpdateLangCacheOp.get_instance(self._cw).add_data((self.entity, 'remove'))


class ServerStartupHook(LangCacheUpdateMixin, Hook):
    """fill-in language caches"""
    __regid__ = 'i18nfield.server-startup'
    events = ('server_startup',)

    def __call__(self):
        session = self.repo.internal_session()
        try:
            op = UpdateLangCacheOp.get_instance(session)
            for lang in session.execute('Any L,C,N WHERE L is I18nLang, '
                                        'L code C, L name N').entities(0):
                self.update_cache(lang, 'set')
        finally:
            session.close()
