from tests.base import TestCase


class HTMLCompressTests(TestCase):

    extensions = ('djinga.ext.htmlcompress.HTMLCompress',)

    def test_always_compress(self):
        self.template = '''
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
        '''

        expected = \
            '''<html><head><title>42</title></head><script type=text/javascript>
                if (foo < 42) {
                  document.write('Foo < Bar');
                }
              </script><body><li><a href="index.html">42</a><br>Test  Foo<li><a href="index.html">42</a><img src=test.png></body></html>'''
        self.assertRender(expected, dict(title=42, href='index.html'))

    def test_leave_spaces_between_vars(self):
        self.template = '''
        {%if True %}
            {{ two }} {{ variables }} in the middle
            of the text
        {% endif %}
        '''
        expected = 'Two variables in the middle of the text'
        self.assertRender(expected, dict(two='Two', variables='variables'))


class SelectiveHTMLCompressTests(TestCase):

    extensions = ('djinga.ext.htmlcompress.SelectiveHTMLCompress',)

    def test_selective_compress(self):
        self.template = '''
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
        '''

        expected = u'''
            Normal   <span>  unchanged </span> stuff
            Stripped <span class=foo  >   test   </span><a href="foo">  test </a> 42Normal <stuff>   again 42  </stuff><p>Foo<br>Bar Baz<p>Moep    <span>Test</span>    Moep</p>
        '''

        self.maxDiff = None
        self.assertRender(expected, dict(foo=42))
