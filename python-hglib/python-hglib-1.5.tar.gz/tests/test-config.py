import os, common, hglib

class test_config(common.basetest):
    def setUp(self):
        common.basetest.setUp(self)
        f = open('.hg/hgrc', 'a')
        f.write('[section]\nkey=value\n')
        f.close()
        self.client = hglib.open()

    def test_basic(self):
        config = self.client.config()

        self.assertTrue(('section', 'key', 'value') in self.client.config())

        self.assertTrue([('section', 'key', 'value')],
                        self.client.config('section'))
        self.assertTrue([('section', 'key', 'value')],
                        self.client.config(['section', 'foo']))
        self.assertRaises(hglib.error.CommandError,
                          self.client.config, ['a.b', 'foo'])

    def test_show_source(self):
        config = self.client.config(showsource=True)

        self.assertTrue((os.path.abspath('.hg/hgrc') + ':2',
                         'section', 'key', 'value') in config)

class test_config_arguments(common.basetest):
    def test_basic(self):
        client = hglib.open(configs=['diff.unified=5', 'a.b=foo'])
        self.assertEqual(client.config('a'), [('a', 'b', 'foo')])
        self.assertEqual(client.config('diff'), [('diff', 'unified', '5')])
