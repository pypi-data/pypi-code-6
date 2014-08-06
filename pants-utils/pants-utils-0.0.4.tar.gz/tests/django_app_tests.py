import unittest

from django.template.context import Context

from pants_utils.django_apps.pexstaticfiles.storages import EggStorage
from pants_utils.django_apps.pexstaticfiles.finders import EggFinder
from pants_utils.django_apps.pextemplate.loaders import EggAppLoader


class PantsUtilsDjangoTestCase(unittest.TestCase):
    def setUp(self):
        self.loader = EggAppLoader()
        self.storage = EggStorage('tests')
        self.finder = EggFinder('tests')

    def test_eggapploader(self):
        template, display_name  = self.loader('tests/index.html')
        self.assertEquals(template.render(Context()), 'hello world\n')

    def test_eggstorage_exists(self):
        self.assertTrue(self.storage.exists("static/staticfile.txt"))
        self.assertFalse(self.storage.exists("static/this/does/not/exist.txt"))

    def test_eggstorage_open(self):
        self.assertEqual(self.storage.open("templates/index.html").read(), 'hello world\n')
        self.assertRaises(IOError, self.storage.open, "THISDOESNTEXIST")

    def test_eggfinder_find(self):
        self.assertIsNotNone(self.finder.find('templates/index.html'))
        self.assertIsNone(self.finder.find('this/does/not/exist'))

    def test_eggfinder_list(self):
        found = self.finder.list([])
        self.assertIn('django_app_tests.py', [file for file, storage in list(found)])
