import pytest
import osf
import modgrammar


def parse_n_objectify(str):
    line = osf.parse_line(str)
    obj = osf.objectify_line(line)
    return obj


def test_unix_time():
    line1 = osf.parse_line("1000001111 A")

    result = osf.objectify_line(line1)

    assert result.time == 1000001111000


def test_unix_time_offset():
    line1 = osf.parse_line("1000001111 A")
    line2 = osf.parse_line("1000001115 B")

    result = osf.objectify_lines([line1, line2])

    assert result[0].time == 0
    assert result[1].time == 4000


def test_hhmmss_time():
    result = parse_n_objectify("01:02:03.123 A")
    assert result.time == 3723123


def test_text():
    result = parse_n_objectify("A")
    assert result.text == "A"


def test_link():
    result = parse_n_objectify("A <foo>")
    assert result.link == "foo"


def test_tags():
    result = parse_n_objectify("A #B #C #Aaaaa")
    assert result.tags == ['B', 'C', 'Aaaaa']


def test_tags_unique():
    result = parse_n_objectify("A #tag1 #tag1")
    assert result.tags == ['tag1']


def test_full():
    result = parse_n_objectify("05:01:05.100 asd <bla> #quote #c")
    assert result.time == 18065100
    assert result.text == "asd"
    assert result.link == "bla"
    assert result.tags == ['quote', 'c']


def test_error():
    header, lines = osf.parse_lines(["1000001111 A", "asd#sdsd"])
    result = osf.objectify_lines(lines)

    assert isinstance(result[0], osf.OSFLine)
    assert isinstance(result[1], modgrammar.ParseError)


def test_empty():
    result = osf.objectify_lines([])

    assert len(result) == 0


def test_invalid_first():
    header, lines = osf.parse_lines(['asd#asdasd'])
    result = osf.objectify_lines(lines)

    assert len(result) == 1
    assert isinstance(result[0], modgrammar.ParseError)

