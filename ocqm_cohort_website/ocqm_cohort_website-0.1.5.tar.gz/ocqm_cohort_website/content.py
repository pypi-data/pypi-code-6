import mistune
import os.path

from . import db
from . import locale
from . import paths


class Cohort(locale.Localized):

    @property
    def statistics(self):
        result = []

        for statistic in self.data.get('statistics', tuple()):
            if 'statistics' in self.data:
                result.append({
                    'name': self.localize_dictionary(statistic),
                    'value': statistic['value']
                })

        return result

    @property
    def contact(self):
        result = []

        for line in self.data.get('contact', tuple()):

            result.append({
                'text': line,
                'is_phone': line.startswith('+'),
                'is_mail': '@' in line
            })

        return result


class Page(locale.Localized):

    @property
    def content(self):
        markdown = (
            db.load_markdown(self.id, self.language)
            or
            db.load_markdown(self.id, self.default_language)
        )

        return mistune.markdown(markdown) if markdown else u''

    @property
    def template(self):
        candidates = [
            os.path.join(paths.get_theme_path(), '{}.html'.format(self.id)),
            os.path.join(paths.get_theme_path(), 'index.html')
        ]

        for candidate in candidates:
            if os.path.exists(candidate):
                return os.path.split(candidate)[-1]  # only return the filename

        return None
