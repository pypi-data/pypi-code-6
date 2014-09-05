"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from huron.menus_manager import get_url
from huron.menus_manager.models import Menu, Item


class MenuTestCase(TestCase):
    def setUp(self):
        menu = Menu.objects.create(name='Main menu', slug='main-menu')
        Item.objects.create(nav_title='Home', url='/', sorting=1,
                            target_blank=False, menu=menu)
        about = Item.objects.create(nav_title='About', url='/about/',
                                    sorting=2, target_blank=False, menu=menu)
        Item.objects.create(nav_title='Team', url='/about/', parent=about,
                            sorting=2, target_blank=False, menu=menu)

    def test_get_url(self):
        self.assertEqual(len(get_url()), 4)

    def test_hierarchies(self):
        menu = Menu.objects.get(slug='main-menu')
        first_level = menu.get_first_level()
        childrens = first_level[1].get_childs()
        self.assertEqual(first_level[0].has_childs(), False)
        self.assertEqual(first_level[1].has_childs(), True)
        self.assertEqual(len(childrens), 1)
        self.assertEqual(len(childrens[0].get_brothers()), 1)
        self.assertEqual(first_level[0].get_brothers(), first_level[0])

    def test_str_menus(self):
        menu = Menu.objects.get(slug='main-menu')
        home = Item.objects.get(pk=1)
        self.assertEqual(str(menu), 'Main menu')
        self.assertEqual(str(home), 'Home')
