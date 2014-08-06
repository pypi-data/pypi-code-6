from tests.base import TestCase


class StaticTests(TestCase):

    extensions = ('djinga.ext.url',)

    def test_reverse_url(self):
        self.template = "{% url 'notfound' %}"
        self.assertRender('/not_found/')
