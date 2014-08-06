from django.test import RequestFactory
from django.template.defaulttags import CsrfTokenNode

from jinja2 import Markup

from tests.base import TestCase


request_factory = RequestFactory()


class DjangoTagsTests(TestCase):

    extensions = ('djinga.ext.django',
                  'djinga.ext.csrf_token')

    def test_django_tag(self):
        # using django specific template tags, without spaces nor linebreaks
        self.template = \
            '{% django %}' \
            '{% load i18n %}' \
            '{% blocktrans %}To be translated{% endblocktrans %}' \
            '{% enddjango %}'
        self.assertRender('To be translated',
                          {'request': request_factory.get('/')})

    def test_django_tag_file(self):
        # using django specific template tags, without spaces nor linebreaks
        self.template_file = 'djangotag/jinja.jjhtml'
        self.assertRender('\n\nTo be translated\n',
                          {'request': request_factory.get('/')})

    def test_csrf_token(self):
        self.template = '{% csrf_token %}'
        csrf_token = 'CSRFTOKEN'
        self.assertRender(
            Markup(CsrfTokenNode().render({'csrf_token': csrf_token})),
            {'csrf_token': csrf_token})
