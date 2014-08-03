import pytest
import osf.classes


def test_str():
    line = osf.classes.OSFLine()
    line.time = 5111000
    line.text = "foo"
    line.link = "http://google.com/"
    line.tags = ['asd', 'foo']
    line.indentation = 5

    assert str(line) == '----- 01:25:11.000 foo <http://google.com/> #asd #foo'


def test_str_no_tags():
    line = osf.classes.OSFLine()
    line.time = 5111000
    line.text = "foo"
    line.link = "http://google.com/"
    line.indentation = 5

    assert str(line) == '----- 01:25:11.000 foo <http://google.com/>'


def test_str_no_link():
    line = osf.classes.OSFLine()
    line.time = 5111000
    line.text = "foo"
    line.indentation = 5

    assert str(line) == '----- 01:25:11.000 foo'


def test_str_no_indentation():
    line = osf.classes.OSFLine()
    line.time = 5111000
    line.text = "foo"

    assert str(line) == '01:25:11.000 foo'


def test_str_no_time():
    line = osf.classes.OSFLine()
    line.text = "foo"

    assert str(line) == 'foo'


def test_str_no_time_plus_indent():
    line = osf.classes.OSFLine()
    line.text = "foo"
    line.indentation = 3

    assert str(line) == '--- foo'
