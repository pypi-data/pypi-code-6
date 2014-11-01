import unittest

from pyramid import testing

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_includeme(self):
        from pyramid.interfaces import ITweens
        from pyramid.tweens import excview_tween_factory
        from ..tweens import iprestrict_tween_factory
        self.config.include('pyramid_iprestrict')
        tweens = self.config.registry.queryUtility(ITweens)
        implicit = tweens.implicit()
        self.assertEqual(
            implicit,
            [
                ('pyramid_iprestrict.tweens.iprestrict_tween_factory',
                 iprestrict_tween_factory),
                ('pyramid.tweens.excview_tween_factory',
                 excview_tween_factory),
            ])
