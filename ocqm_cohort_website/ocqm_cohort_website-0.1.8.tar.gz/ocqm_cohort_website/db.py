import codecs
import os.path
import yaml


def load_metadata():
    return load_metadata_by_path('cohort.yml')


def load_metadata_by_path(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return yaml.load(f.read())


def load_markdown(name, language):
    return load_markdown_by_path('pages/{}.{}.md'.format(name, language))


def load_markdown_by_path(path):
    if os.path.exists(path):
        with codecs.open(path, 'r', 'utf-8') as f:
            return f.read()
