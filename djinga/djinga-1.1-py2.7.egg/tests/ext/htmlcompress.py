from django.utils.unittest import TestCase

from jinja2 import Environment

from djinga.ext.htmlcompress import HTMLCompress, SelectiveHTMLCompress


class HTMLCompressTests(TestCase):

    def test_always_compress(self):
        env = Environment(extensions=[HTMLCompress])
        tmpl = env.from_string('''
            <html>
              <head>
                <title>{{ title }}</title>
              </head>
              <script type=text/javascript>
                if (foo < 42) {
                  document.write('Foo < Bar');
                }
              </script>
              <body>
                <li><a href="{{ href }}">{{ title }}</a><br>Test  Foo
                <li><a href="{{ href }}">{{ title }}</a><img src=test.png>
              </body>
            </html>
        ''')

        self.assertEqual(tmpl.render(title=42, href='index.html'),
           '''<html><head><title>42</title></head><script type=text/javascript>
                if (foo < 42) {
                  document.write('Foo < Bar');
                }
              </script><body><li><a href="index.html">42</a><br>Test  Foo<li><a href="index.html">42</a><img src=test.png></body></html>''')

    def test_selective_compress(self):
        env = Environment(extensions=[SelectiveHTMLCompress])
        tmpl = env.from_string('''
            Normal   <span>  unchanged </span> stuff
            {% strip %}Stripped <span class=foo  >   test   </span>
            <a href="foo">  test </a> {{ foo }}
            Normal <stuff>   again {{ foo }}  </stuff>
            <p>
              Foo<br>Bar
              Baz
            <p>
              Moep    <span>Test</span>    Moep
            </p>
            {% endstrip %}
        ''')

        expected = u'''
            Normal   <span>  unchanged </span> stuff
            Stripped <span class=foo  >   test   </span><a href="foo">  test </a> 42Normal <stuff>   again 42  </stuff><p>Foo<br>Bar Baz<p>Moep    <span>Test</span>    Moep</p>
        '''

        self.maxDiff = None
        self.assertEqual(tmpl.render(foo=42), expected)

    def test_leave_spaces_between_vars(self):
        env = Environment(extensions=[HTMLCompress])
        tmpl = env.from_string('''
        {%if True %}
            {{ two }} {{ variables }} in the middle
            of the text
        {% endif %}
        ''')

        self.assertEqual(tmpl.render(two='Two', variables='variables'),
                         'Two variables in the middle of the text')
