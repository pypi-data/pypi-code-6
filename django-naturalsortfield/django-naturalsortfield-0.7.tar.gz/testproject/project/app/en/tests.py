import unittest

from project.app.en.models import NaturalSortModelEn

class NaturalSortFieldEnTestCase(unittest.TestCase):
    def test_order(self):
        NaturalSortModelEn.objects.create(title='The XYZ 3')
        NaturalSortModelEn.objects.create(title='XYZ 1')
        NaturalSortModelEn.objects.create(title='XYZ 10')
        NaturalSortModelEn.objects.create(title='XYZ 2')
        
        self.assertEqual(
            ['XYZ 1', 'XYZ 2', 'The XYZ 3', 'XYZ 10'],
            [
                obj.title
                for obj in NaturalSortModelEn.objects.order_by('natural_title')
            ]
        )
