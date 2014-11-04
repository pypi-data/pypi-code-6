from __future__ import with_statement

import unittest
import types

from cwtags import tag, tagbuilder

class TestTagsTC(unittest.TestCase):

    def test_all_tags(self):
        tagnames = set(dir(tag))
        tagnames.remove('tag')
        for tname in sorted(tagnames):
            t = getattr(tag, tname)
            if not isinstance(t, types.FunctionType):
                continue
            if tname in tagbuilder.HTML_EMPTY_TAGS:
                self.assertIn(tname, unicode(t(id='babar')))
            else:
                self.assertIn(tname, unicode(t()))

    def test_simple_tags(self):
        self.assertEqual(unicode(tag.div(u'toto', Class="css")),
                         u'<div class="css">toto</div>')
        self.assertEqual(unicode(tag.div(u'toto',
                                         tag.p(u'titi', data_foo=42),
                                         tag.img(src='www.perdu.com'),
                                         id='foo')),
                         u'<div id="foo">toto<p data-foo="42">titi</p><img src="www.perdu.com"/></div>')

    def test_context_tags(self):
        parent = tagbuilder.UStringIO()
        with tag.div(parent.write, title=u'what it does') as d:
            d(tag.p(u'oups'))
            with tag.table(d) as t:
                t(tag.a(u'perdu !', href=u'www.perdu.com'))
                t(tag.input(type='hidden'))
        self.assertEqual(parent.getvalue(),
                         u'<div title="what it does"><p>oups</p><table>'
                         '<a href="www.perdu.com">perdu !</a><input type="hidden"/>'
                         '</table>\n</div>\n')

    def test_context_tags_withsomemethod(self):
        parent = list()
        with tag.div(parent.append, title=u'what it does') as d:
            d(tag.p(u'oups'))
            with tag.table(d) as t:
                t(tag.a(u'perdu !', href=u'www.perdu.com'))
                t(tag.input(type='hidden'))
        self.assertEqual(''.join(str(x) for x in parent),
                         u'<div title="what it does"><p>oups</p><table>'
                         '<a href="www.perdu.com">perdu !</a><input type="hidden"/>'
                         '</table>\n</div>\n')

    def _write_in_the_back(self, text):
        self.w(tag.span(text))

    def test_context_tags_interleaving(self):
        parent = tagbuilder.UStringIO()
        self.w = parent.write
        with tag.div(self.w, title='okay') as d:
            d(tag.p(u'hum'))
            self._write_in_the_back(u'uhuh')
            self.w(tag.p(u'yo'))
        self.assertEqual(parent.getvalue(),
                         u'<div title="okay"><p>hum</p><span>uhuh</span><p>yo</p></div>\n')

    def test_error(self):
        with self.assertRaises(TypeError) as cm:
            with tag.div(12):
                pass
        self.assertEqual(str(cm.exception),
                         'Did you forget to give a callable in first position ?')

    def test_monkeypatch_does_not_break_assert(self):
        parent = tagbuilder.UStringIO()
        w = parent.write
        self.assertRaises(AssertionError, w, 42)

    def test_tag_names(self):
        expected = u'<div class="css"></div>'
        self.assertEqual(unicode(tag.div(Class='css')), expected)
        self.assertEqual(unicode(tag.div(class_='css')), expected)
        self.assertEqual(unicode(tag.div(_class='css')), expected)
        self.assertEqual(unicode(tag.div(klass='css')), expected)

    def test_flag_tags(self):
        self.assertEqual(
            unicode(tag.option(u'test', value='5', selected=True)),
            u'<option selected value="5">test</option>')
        self.assertEqual(
            unicode(tag.option(u'test', value='5', selected=False)),
            u'<option value="5">test</option>')

    def test_none_tags(self):
        self.assertEqual(unicode(tag.div(title=None)),
                         u'<div ></div>')

    def test_list_tags(self):
        classes = ['css1', 'css2']
        expected = [u'<div class="css1 css2"></div>',
                    u'<div class="css2 css1"></div>']
        self.assertIn(unicode(tag.div(class_=classes)), expected)
        self.assertIn(unicode(tag.div(class_=tuple(classes))), expected)

        self.assertIn(unicode(tag.div(class_=set(classes))), expected)
        self.assertIn(unicode(tag.div(class_=frozenset(classes))), expected)

    def test_dict_tags(self):
        classes = {'css1': True, 'css2': False}
        expected = u'<div class="css1"></div>'
        self.assertEqual(unicode(tag.div(class_=classes)), expected)


if __name__ == '__main__':
    unittest.main()
