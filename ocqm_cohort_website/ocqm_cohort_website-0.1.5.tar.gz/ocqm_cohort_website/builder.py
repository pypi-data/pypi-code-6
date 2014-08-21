import os

from babel.support import Translations
from copy import copy
from jinja2 import Environment, FileSystemLoader

from . import content
from . import db
from . import locale
from . import paths


def create_environment(theme_path, language):

    loader = FileSystemLoader(searchpath=theme_path, encoding='utf-8')
    environment = Environment(loader=loader, extensions=['jinja2.ext.i18n'])

    translations = Translations.load(paths.get_locale_path(), language)
    environment.install_gettext_translations(translations)

    # global functions available in the templates
    environment.globals.update(get_language_name=locale.get_language_name)

    return environment


def include_paths_in_output(include_paths, output_path):

    for include_path in include_paths:
        paths.copy_files(
            include_path,
            os.path.join(output_path, os.path.split(include_path)[-1])
        )


def render(theme_path, output_path, language, shared_context, pages):
    # load jinja2 environment
    env = create_environment(theme_path, language)

    for page in pages:
        template = env.get_template(page.template)

        context = copy(shared_context)
        context.update({
            'page': page,
            'pages': pages
        })

        template.stream(**context).dump(
            os.path.join(output_path, '{}.html'.format(page.id)), 'utf-8'
        )


def build_breadcrumbs(pages, current_page):
    if current_page.id == pages[0].id:  # root page
        return (
            (current_page.id, current_page.title),
        )
    else:
        return (
            (pages[0].id, pages[0].title),
            (current_page.id, current_page.title),
        )


def build_site(output_path):

    metadata = db.load_metadata()

    assert metadata, """
        No metadata was found in path {}
    """.format(output_path)

    # the first language is the default language; the default language is
    # stored in the root path, others in the ./[lang] path
    languages = metadata['languages']
    default_language = languages[0]

    # the ./media directory in the user data directory will be included
    # in the output if it is available
    content_media = os.path.join(os.getcwd(), 'media')

    for language in languages:

        # create the correct directory if necessary
        if language != default_language:
            output_path = os.path.join(output_path, language)

        paths.ensure_directory(output_path)

        # load the cohort
        cohort = content.Cohort(metadata, languages, language)

        # load the pages
        assert len(metadata['pages']) == 5, """
            Define exactly 5 pages (with index)
        """

        pages = [
            content.Page(p, languages, language) for p in metadata['pages']
        ]

        # build the navigation
        for page in pages:
            page.breadcrumbs = build_breadcrumbs(pages, page)

        # render the templates
        render(
            theme_path=paths.get_theme_path(),
            output_path=output_path,
            language=language,
            shared_context={
                'cohort': cohort,
                'pages': pages
            },
            pages=pages
        )

        # copy the static files
        if os.path.exists(content_media):
            include_paths = (paths.get_static_path(), content_media)
        else:
            include_paths = (paths.get_static_path(), )

        include_paths_in_output(include_paths, output_path)
