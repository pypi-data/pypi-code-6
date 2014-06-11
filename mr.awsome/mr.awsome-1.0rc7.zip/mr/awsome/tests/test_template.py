from mr.awsome.template import Template
from unittest2 import TestCase
import pytest


class TemplateTests(TestCase):
    @pytest.fixture(autouse=True)
    def setup_tempdir(self, tempdir):
        self.tempdir = tempdir
        self.template = tempdir['template.txt']
        self.template_path = self.template.path
        self._fillTemplate = self.template.fill

    def testEmpty(self):
        self._fillTemplate("")
        template = Template(self.template_path)
        result = template()
        self.assertMultiLineEqual(result, "")

    def testPreFilter(self):
        self._fillTemplate("\n".join(str(x) for x in range(3)))
        template = Template(self.template_path, pre_filter=lambda x: x.replace("1\n", ""))
        result = template()
        self.assertMultiLineEqual(result, "0\n2")

    def testPostFilter(self):
        self._fillTemplate("\n".join(str(x) for x in range(3)))
        template = Template(self.template_path, post_filter=lambda x: x.replace("1\n", ""))
        result = template()
        self.assertMultiLineEqual(result, "0\n2")

    def testKeywordOption(self):
        self._fillTemplate("{option}")
        template = Template(self.template_path)
        result = template(option="foo")
        self.assertMultiLineEqual(result, "foo")

    def testBase64Option(self):
        self._fillTemplate("option: base64 1\n\n{option}")
        template = Template(self.template_path)
        result = template()
        self.assertMultiLineEqual(result, "MQ==\n")
        self.assertMultiLineEqual(result.decode('base64'), "1")

    def testEscapeEolOption(self):
        self._fillTemplate("option: file,escape_eol test.txt\n\n{option}")
        template = Template(self.template_path)
        self.tempdir['test.txt'].fill("1\n2\n")
        result = template()
        self.assertMultiLineEqual(result, "1\\n2\\n")

    def testFileOption(self):
        self._fillTemplate("option: file test.txt\n\n{option}")
        template = Template(self.template_path)
        self.tempdir['test.txt'].fill("1")
        result = template()
        self.assertMultiLineEqual(result, "1")

    def testFormatOption(self):
        self._fillTemplate("option: format {foo}\n\n{option}")
        template = Template(self.template_path)
        result = template(foo=1)
        self.assertMultiLineEqual(result, "1")

    def testGzipOption(self):
        self._fillTemplate("option: gzip,base64 1\n\n{option}")
        template = Template(self.template_path)
        result = template()
        payload = result.decode('base64')
        header = payload[:10]
        body = payload[10:]
        self.assertEqual(header[:4], "\x1f\x8b\x08\x00")  # magic + compression + flags
        self.assertEqual(header[8:], "\x02\xff")  # extra flags + os
        self.assertEqual(body, "3\x04\x00\xb7\xef\xdc\x83\x01\x00\x00\x00")

    def testTemplateOption(self):
        self._fillTemplate("template: template test.txt\n\n{template}")
        template = Template(self.template_path)
        self.tempdir['test.txt'].fill("option: format 1\n\n{option}")
        result = template()
        self.assertMultiLineEqual(result, "1")

    def testUnkownOption(self):
        self._fillTemplate("option: foo 1\n\n{option}")
        template = Template(self.template_path)
        with pytest.raises(ValueError):
            template()
