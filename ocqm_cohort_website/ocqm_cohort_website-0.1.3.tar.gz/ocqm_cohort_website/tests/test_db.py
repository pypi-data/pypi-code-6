import os
import yaml

from .. import db


def test_get_metadata(temp_directory):
    with open('cohort.yml', 'w') as outfile:
        outfile.write(yaml.dump({'foo': 'bar'}))

    assert db.load_metadata() == {'foo': 'bar'}


def test_get_markdown(temp_directory):
    os.mkdir('pages')

    with open('pages/test.en.md', 'w') as f:
        f.write('test')

    assert db.load_markdown('test', 'en') == 'test'
