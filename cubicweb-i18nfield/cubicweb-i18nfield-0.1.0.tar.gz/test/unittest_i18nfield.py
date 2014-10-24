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

from datetime import datetime as dt, timedelta as td

from cubicweb import ValidationError, Unauthorized
from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.web.views.autoform import InlinedFormField

from cubes.i18nfield.utils import LANGS_BY_CODE, LANGS_BY_EID

#import logging
#logging.getLogger().setLevel(0)


class I18nFieldTC(CubicWebTC):

    def setup_database(self):
        super(I18nFieldTC, self).setup_database()
        req = self.request()
        self.en = req.create_entity('I18nLang', code=u'en', name=u'English')
        self.fr = req.create_entity('I18nLang', code=u'fr', name=u'French')
        self.de = req.create_entity('I18nLang', code=u'de', name=u'German')
        req.set_shared_data('i18nfield_lang', {u'title': u'fr'})
        self.card = req.create_entity('Card', title=u'salut',
                                      ref_lang=self.fr)
        self.commit()

    def create_card(self, cnx, title):
        return cnx.create_entity('Card', title=title,
                                      ref_lang=self.fr)

    def test_entity(self):
        # Check translatable printable_value and related adapter's methods
        req = self.card._cw # use req.data when calling self.card.dc_title
        tr_en = req.create_entity('Translation', value=u'hello', lang=self.en,
                                  of_field=self.card.reverse_i18nfield_of[0])
        self.commit()
        req.data['i18nfield_target_lang'] = u'fr'
        self.assertEqual(self.card.dc_title(), u'salut')
        req.data['i18nfield_target_lang'] = u'en'
        self.assertEqual(self.card.dc_title(), u'hello')
        # Check I18nField methods
        field = self.card.reverse_i18nfield_of[0]
        self.assertEqual(field.translation(u'en').value, u'hello')
        self.assertEqual(field.original_value(), u'salut')
        # Check Translation methods
        self._set_field_last_edited(field, dt.now())
        self.failUnless(tr_en.is_outdated())
        # Check adapter's translation_infos method
        adapted = self.card.cw_adapt_to('translatable_entity')
        tr_infos = adapted.translation_infos()
        # - english
        en_infos = tr_infos[0]
        self.assertEqual(en_infos[0].eid, self.en.eid)
        self.assertEqual(len(en_infos[1]), 1) # one field only
        self.assertEqual(en_infos[1][0][0].eid, tr_en.eid)
        self.assertEqual(en_infos[1][0][1].eid, field.eid)
        # - german
        de_infos = tr_infos[1]
        self.assertEqual(de_infos[0].eid, self.de.eid)
        self.assertEqual(de_infos[1], None)

    def _assert_is_fresh(self, field):
        field.cw_clear_all_caches()
        self.failUnless(dt.now() - field.last_edited < td(seconds=10))

    def _set_field_last_edited(self, field, date):
        session = self.repo.internal_session()
        try:
            session.execute('SET X last_edited %(d)s WHERE X eid %(x)s',
                            {'x': field.eid, 'd': date})
            session.commit()
        finally:
            session.close()
        field.cw_clear_all_caches()
        self.assertEqual(field.last_edited, date)

    def test_translatable_hooks(self):
        # check creation hook: I18nField creation with supplied lang...
        req = self.card._cw
        self.failUnless(self.card.reverse_i18nfield_of)
        field = self.card.reverse_i18nfield_of[0]
        # ... and correct last_edited date
        self._assert_is_fresh(field)
        # edition hook: last_edited must be updated
        self._set_field_last_edited(field, dt.now() - td(days=10))
        self.card.cw_set(title=u'bonjour')
        self.commit()
        field.cw_clear_all_caches()
        self.failUnless(dt.now() - field.last_edited < td(seconds=1))
        # deletion hook
        req.execute('DELETE Card C WHERE C eid %(c)s', {'c': self.card.eid})
        self.commit()
        self.failIf(req.execute('Any F WHERE F eid %(x)s',
                                {'x': field.eid}).rowcount)

    def test_lang_cache_dicts_hooks(self):
        req = self.en._cw
        init_codes = [u'de', u'en', u'fr']
        init_eids = sorted([self.en.eid, self.fr.eid, self.de.eid])
        self.assertEqual(sorted(LANGS_BY_CODE.keys()), init_codes)
        self.assertEqual(sorted(LANGS_BY_EID.keys()), init_eids)
        # test creation
        sp = req.create_entity('I18nLang', code=u'sp', name=u'Spanish')
        self.commit()
        self.assertEqual(sorted(LANGS_BY_CODE.keys()), init_codes + [u'sp'])
        self.assertEqual(sorted(LANGS_BY_EID.keys()), init_eids + [sp.eid])
        # test update
        sp.cw_set(code=u'sq')
        self.commit()
        self.assertEqual(sorted(LANGS_BY_CODE.keys()), init_codes + [u'sq'])
        self.assertEqual(sorted(LANGS_BY_EID.keys()), init_eids + [sp.eid])
        # test remove
        req.execute('DELETE I18nLang L WHERE L code "sq"')
        self.commit()
        self.assertEqual(sorted(LANGS_BY_CODE.keys()), init_codes)
        self.assertEqual(sorted(LANGS_BY_EID.keys()), init_eids)

    def test_constraint(self):
        req = self.card._cw
        tr_fr = req.create_entity('Translation', value=u'salut', lang=self.fr,
                                  of_field=self.card.reverse_i18nfield_of[0])
        self.assertRaises(ValidationError, self.commit)

    def test_permission_admin_cannot_add_i18nfield(self):
        req = self.card._cw
        with self.assertRaises(Unauthorized) as wraperr:
            req.create_entity('I18nField', field_name=u'synopsis',
                              i18nfield_of=self.card)
        self.assertEqual(str(wraperr.exception),
                         ('You are not allowed to perform add operation on '
                          'relation I18nField i18nfield_of Card'))

    def test_unique_together(self):
        req = self.card._cw
        with self.session.repo.internal_session() as session:
            with self.assertRaises(ValidationError) as wraperr:
                session.create_entity('I18nField', field_name=u'title',
                                      i18nfield_of=self.card)
        self.assertDictEqual(
            {'i18nfield_of': u'i18nfield_of is part of violated unicity constraint',
             'field_name': u'field_name is part of violated unicity constraint',
             'unicity constraint': u'some relations violate a unicity constraint'},
            wraperr.exception.args[1])

    def _first_inlined_form(self, form):
        return [field.view.form for field in form.fields
                if isinstance(field, InlinedFormField)][0]

    def _card_form(self, req, vid):
        return req.vreg['forms'].select(vid, req, rset=self.card.as_rset())

    def test_formfield(self):
        '''translation value field and widget classes must be the same as the
        translated field of the original entity'''
        req = self.request()
        req.form['lang_code'] = u'fr'
        # get card translation value field
        tr_card_form = self._card_form(req, 'translate_entity')
        title_form = self._first_inlined_form(tr_card_form)
        tr_form = self._first_inlined_form(title_form)
        tr_card_field = tr_form.field_by_name('value', 'subject')
        # get card title field
        std_form = self._card_form(req, 'edition')
        std_field = std_form.field_by_name('title', 'subject')
        # check field and widget classes
        self.assertEqual(type(tr_card_field), type(std_field))
        self.assertEqual(type(tr_card_field.widget), type(std_field.widget))

    def test_adaptable_i18field(self):
        """test  _TranslatableEntityAdapter.i18nfield method"""
        adapted = self.card.cw_adapt_to('translatable_entity')
        self.assertEqual(adapted.i18nfield('title').field_name, u'title')

    def test_translatable_entity_udpate(self):
        '''test TranslatableEntityUpdateHook'''
        cnx = self.fr._cw
        card1 = self.create_card(cnx, u'title')
        card2 = self.create_card(cnx, u'card2')
        self.commit()
        i18ntitle1 = card1.cw_adapt_to('translatable_entity').i18nfield('title')
        i18ntitle2 = card2.cw_adapt_to('translatable_entity').i18nfield('title')
        initial_date1 = i18ntitle1.last_edited
        initial_date2 = i18ntitle2.last_edited
        # check title i18nfield last_edited date is not changed when
        # another card1 attribute is edited
        card1.cw_set(synopsis=u'synopsis1')
        self.commit()
        i18ntitle1.cw_clear_all_caches()
        self.assertEqual(initial_date1, i18ntitle1.last_edited)
        # check title1 i18nfield last_edited date is changed when card1's title
        # is edited
        initial_date1 = i18ntitle1.last_edited
        card1.cw_set(title=u'card1')
        self.commit()
        i18ntitle1.cw_clear_all_caches()
        self.assertTrue(initial_date1 < i18ntitle1.last_edited)
        # check card2's title i18nfield last_edited date was never updated
        i18ntitle2.cw_clear_all_caches()
        self.assertEqual(initial_date2, i18ntitle2.last_edited)


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
