import os

from collections import namedtuple
from pytest import raises

from .. import builder
from .. import paths


def test_create_environment(temp_directory):

    # just a smoke test
    assert builder.create_environment(temp_directory, 'de')


def test_build_breadcrumbs():
    Page = namedtuple('Page', ['id', 'title'])

    pages = [
        Page('root', 'Root'),
        Page('child', 'Child')
    ]

    breadcrumbs = builder.build_breadcrumbs(pages, current_page=pages[0])
    assert len(breadcrumbs) == 1
    assert breadcrumbs[0][0] == 'root'

    breadcrumbs = builder.build_breadcrumbs(pages, current_page=pages[1])
    assert len(breadcrumbs) == 2
    assert breadcrumbs[0][0] == 'root'
    assert breadcrumbs[1][0] == 'child'


def test_build_demo(temp_directory):
    with paths.switch_path(paths.get_example_path()):
        builder.build_site(temp_directory)

    os.path.exists(os.path.join(temp_directory, 'index.html'))
    os.path.exists(os.path.join(temp_directory, 'media'))

    os.path.exists(os.path.join(temp_directory, 'de', 'index.html'))
    os.path.exists(os.path.join(temp_directory, 'de', 'media'))

    with open(os.path.join(temp_directory, 'index.html'), 'r') as f:
        english = f.read()

    with open(os.path.join(temp_directory, 'de', 'index.html'), 'r') as f:
        german = f.read()

    assert 'Demo Cohort' in english
    assert 'more' in english
    assert '<li class="selected">English</li>' in english

    assert 'Demo Kohorte' in german
    assert 'mehr' in german
    assert '<li class="selected">Deutsch</li>' in german


def test_language_nesting(temp_directory):
    metadata = {
        'languages': ['en', 'de', 'fr'],
        'pages': [
            {'id': 'index', 'title': 'Index'},
            {'id': '1', 'title': 'One'},
            {'id': '2', 'title': 'Two'},
            {'id': '3', 'title': 'Three'},
            {'id': '4', 'title': 'Four'}
        ]
    }

    builder.build_site(temp_directory, metadata)

    assert 'de' in os.listdir(temp_directory)
    assert 'fr' in os.listdir(temp_directory)
    assert 'index.html' in os.listdir(temp_directory)

    assert 'de' not in os.listdir(os.path.join(temp_directory, 'de'))
    assert 'fr' not in os.listdir(os.path.join(temp_directory, 'de'))
    assert 'index.html' in os.listdir(os.path.join(temp_directory, 'de'))

    assert 'de' not in os.listdir(os.path.join(temp_directory, 'fr'))
    assert 'fr' not in os.listdir(os.path.join(temp_directory, 'fr'))
    assert 'index.html' in os.listdir(os.path.join(temp_directory, 'fr'))


def test_no_metadata(temp_directory):
    with raises(AssertionError):
        builder.build_site(temp_directory)
