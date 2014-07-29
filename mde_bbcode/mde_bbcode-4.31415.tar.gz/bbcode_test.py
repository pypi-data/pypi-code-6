#!/bin/env python
# -*- coding: utf-8 -*-

import bbcode
import html
import time

import unittest


class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = bbcode.BbCodeParser()

    def check(self, bbcode, expected_html):
        self.assertEqual(self.parser.parse(bbcode), expected_html)


class TestConvertSimpleTokens(ParserTestCase):
    def test_inline(self):
        self.check("[b]fett[/b]", "<Strong>fett</Strong>")
        self.check("[i]kursiv[/i]", "<Em>kursiv</Em>")
        self.check("[s]durchgestrichen[/s]", "<Strike>durchgestrichen</Strike>")
        self.check("[m]inline code[/m]", "<InlineCode>inline code</InlineCode>")

    def test_blocks(self):
        self.check("[code]code block[/code]", "<Code>code block</Code>")
        self.check("[php]php code block[/php]", "<Code Language=\"PHP\">php code block</Code>")
        self.check("[spoiler]spoiler[/spoiler]", "<Spoiler>spoiler</Spoiler>")

    def test_mod(self):
        self.check("[mod]moderator text[/mod]", "<Highlight>moderator text</Highlight>")

    def test_url(self):
        self.check("[url]http://tempuri.org[/url]", "<Link Target=\"http://tempuri.org\" />")
        self.check("[url=http://tempuri.org]Link name[/url]", "<Link Target=\"http://tempuri.org\">Link name</Link>")
        self.check("[img]http://tempuri.org/Image.png[/img]", "<Image Source=\"http://tempuri.org/Image.png\" />")

    def test_list(self):
        self.check("[list][*]erstens[*]zweitens[*]drittens[/list]",
                   "<List><Item>erstens</Item><Item>zweitens</Item><Item>drittens</Item></List>")

    def test_quote(self):
        self.check("[quote]zitat ohne autor[/quote]", "<Quote>zitat ohne autor</Quote>")
        self.check("[quote=123,456,\"[DK]Peacemaker\"]zitat von autor mit sonderzeichen[/quote]",
                   "<Quote ThreadId=\"123\" PostId=\"456\" Author=\"[DK]Peacemaker\">zitat von autor "
                   "mit sonderzeichen</Quote>")

    def test_table(self):
        self.check("[table]1[||]2[--]3[||]4[/table]",
                   "<Table><Row><Cell>1</Cell><Cell>2</Cell></Row><Row><Cell>3</Cell><Cell>4</Cell></Row></Table>")


class TestNestedTokens(ParserTestCase):
    def test_inline(self):
        self.check("[b][i]fett und kursiv[/i][/b]", "<Strong><Em>fett und kursiv</Em></Strong>")
        self.check("[b][i][s][u][m]verschachtelt[/m][/u][/s][/i][/b]",
                   "<Strong><Em><Strike><Underline><InlineCode>verschachtelt</InlineCode></Underline>"
                   "</Strike></Em></Strong>")

    def test_quote(self):
        self.check("[quote]kein autor[quote=123,456,\"Author\"]mit autor[/quote]ok?[/quote]",
                   "<Quote>kein autor<Quote ThreadId=\"123\" PostId=\"456\" Author=\"Author\">mit "
                   "autor</Quote>ok?</Quote>")

    def test_list(self):
        self.check("[list][*][b]fett[/b][*][i]kursiv[/i][/list]",
                   "<List><Item><Strong>fett</Strong></Item><Item><Em>kursiv</Em></Item></List>")


class TestMissingEndTokens(ParserTestCase):
    def test_missing(self):
        self.check("[b][i]fett und kursiv[/b]", "<Strong><Em>fett und kursiv</Em></Strong>")
        self.check("[b]fett", "<Strong>fett</Strong>")
        self.check("[quote]zitat von [b]autor[quote]weiteres zitat[/quote]",
                   "<Quote>zitat von <Strong>autor<Quote>weiteres zitat</Quote></Strong></Quote>")

    def test_swapped(self):
        self.check("[b][i]fett und kursiv, aber vertauscht[/b][/i]",
                   "<Strong><Em>fett und kursiv, aber vertauscht</Em></Strong>")
        self.check("[b]Hallo[i]Welt[/b]![/i]", "<Strong>Hallo<Em>Welt</Em></Strong><Em>!</Em>")
        self.check("[u][b]Hallo[i][s]Welt[/b][/u]![/s][/i]",
                   "<Underline><Strong>Hallo<Em><Strike>Welt</Strike></Em></Strong></Underline><Em>"
                   "<Strike>!</Strike></Em>")


class TestParameterLiterals(ParserTestCase):
    def test_literals(self):
        self.check("[quote=\"123\", \"456\", \"Author\"]Zitat[/quote]",
                   "<Quote ThreadId=\"123\" PostId=\"456\" Author=\"Author\">Zitat</Quote>")
        self.check("[url=\"http://tempuri.org\"]Name[/url]",
                   "<Link Target=\"http://tempuri.org\">Name</Link>")


class TestIgnoreCase(ParserTestCase):
    def test_ignore_case(self):
        self.check("[B]fett[/b]", "<Strong>fett</Strong>")
        self.check("[I]kursiv[/i]", "<Em>kursiv</Em>")
        self.check("[S]durchgestrichen[/s]", "<Strike>durchgestrichen</Strike>")
        self.check("[M]inline code[/m]", "<InlineCode>inline code</InlineCode>")
        self.check("[CODE]code block[/code]", "<Code>code block</Code>")
        self.check("[PHP]php code block[/php]", "<Code Language=\"PHP\">php code block</Code>")
        self.check("[SPOILER]spoiler[/spoiler]", "<Spoiler>spoiler</Spoiler>")
        self.check("[MOD]moderator text[/mod]", "<Highlight>moderator text</Highlight>")
        self.check("[URL]http://tempuri.org[/url]", "<Link Target=\"http://tempuri.org\" />")
        self.check("[URL=http://tempuri.org]Link name[/url]", "<Link Target=\"http://tempuri.org\">Link name</Link>")
        self.check("[IMG]http://tempuri.org/Image.png[/img]", "<Image Source=\"http://tempuri.org/Image.png\" />")
        self.check("[LIST][*]erstens[*]zweitens[*]drittens[/list]",
                   "<List><Item>erstens</Item><Item>zweitens</Item><Item>drittens</Item></List>")
        self.check("[QUOTE]zitat ohne autor[/quote]", "<Quote>zitat ohne autor</Quote>")
        self.check("[QUOTE=123,456,\"[DK]Peacemaker\"]zitat von autor mit sonderzeichen[/quote]",
                   "<Quote ThreadId=\"123\" PostId=\"456\" Author=\"[DK]Peacemaker\">zitat von autor mit"
                   " sonderzeichen</Quote>")


class TestAssortedKlappfallscheiben(ParserTestCase):
    def test_klapp_fall_scheibe(self):
        self.check("[b] Fett </Strong> [/b]", "<Strong> Fett &lt;/Strong&gt; </Strong>")
        self.check("[url=\"123]url[/url]", "[url=\"123]url[/url]")
        self.check("[url=\"123]\"]url[/url]", "<Link Target=\"123]\">url</Link>")
        self.check("[quote=123,456,\"ABC", "[quote=123,456,\"ABC")
        self.check("[quote=123,456,\"ABC\" ]Test[/quote]",
                   "<Quote ThreadId=\"123\" PostId=\"456\" Author=\"ABC\">Test</Quote>")
        self.check("[quote=\"Welt\"][quote=123,456,\"Ernie\"]Hallo Welt![/quote]Hallo Ernie![/quote]",
                   "[quote=\"Welt\"]<Quote ThreadId=\"123\" PostId=\"456\" Author=\"Ernie\">Hallo Welt!</Quote>"
                   "Hallo Ernie![/quote]")
        self.check("[list]Hallo [*]Welt [*]! [/list]",
                   "<List><Item>Hallo </Item><Item>Welt </Item><Item>! </Item></List>")
        self.check("[list][*]Dies[*]ist[list][*]eine[*]verschachtelte[/list][*]Liste![/list]",
                   "<List><Item>Dies</Item><Item>ist<List><Item>eine</Item><Item>verschachtelte</Item></List></Item>"
                   "<Item>Liste!</Item></List>")
        self.check('Hallo Welt! [quote = 123 , 456 , "Ernie" ]Das ist doch nicht [b]dein[/b] Ernst?![/quote]',
                   'Hallo Welt! <Quote ThreadId="123" PostId="456" Author="Ernie">Das ist doch nicht <Strong>dein'
                   '</Strong> Ernst?!</Quote>')
        self.check("[code]Other [b]Tags[/b] inside Code-Tags[/code]", "<Code>Other [b]Tags[/b] inside Code-Tags</Code>")


if __name__ == '__main__':
    unittest.main()
