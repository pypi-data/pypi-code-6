import i18n, pkg_resources

from hexlet.logger import Logger

locale_path = pkg_resources.resource_filename(__name__, 'locales')
i18n.load_path.append(locale_path)
i18n.set("locale", "en")
i18n.set("error_on_missing_translation", True)
i18n.set("error_on_missing_placeholder", True)

host = "hexlet.org"
lesson_template_path = "resources/lesson"
