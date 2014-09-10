from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError, connection, reset_queries
from django.template import Context, Template
from django.test import TestCase

from django_tiniest_cms.models import Content

TEMPLATE = Template("""{% load tiniest_cms %}
{% content 'root' %}
default stuff
{% endcontent %}
""")

CONTEXT = Context(dict())

class ContentTestCase(TestCase):
    def setUp(self):
        settings.DEBUG = True
        cache.clear()

    def test_content_names_are_unique(self):
        Content.objects.create(name='root', content='different')
        with self.assertRaises(IntegrityError):
            Content.objects.create(name='root', content='different')

    def test_no_content(self):
        self.assertIn('default stuff', TEMPLATE.render(CONTEXT))

    def test_with_content(self):
        Content.objects.create(name='root', content='different')
        reset_queries()
        self.assertIn('different', TEMPLATE.render(CONTEXT))
        self.assertEqual(len(connection.queries), 1)

    def test_content_rendered_as_markdown(self):
        Content.objects.create(
            name='root',
            content='*embiggen* and **cromulent**'
        )
        self.assertIn('<em>embiggen</em>', TEMPLATE.render(CONTEXT))

    def test_html_content_escaped(self):
        Content.objects.create(name='root', content='<script>CSRF</script>')
        self.assertNotIn('<script>CSRF</script>', TEMPLATE.render(CONTEXT))

    def test_content_cached(self):
        Content.objects.create(name='root', content='different')
        reset_queries()
        TEMPLATE.render(CONTEXT) # first rendering
        TEMPLATE.render(CONTEXT) # second rendering
        self.assertEqual(len(connection.queries), 1)

    def test_content_cache_updated_on_save(self):
        content = Content.objects.create(name='root', content='different')
        self.assertIn('different', TEMPLATE.render(CONTEXT))

        content.content = 'other'
        content.save()

        self.assertIn('other', TEMPLATE.render(CONTEXT))
