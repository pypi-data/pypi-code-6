import i18n, pkg_resources
from os import path

from hexlet.logger import Logger

locale_path = pkg_resources.resource_filename(__name__, path.join('data', 'locales'))
i18n.load_path.append(locale_path)
i18n.set("locale", "en")
i18n.set("error_on_missing_translation", True)
i18n.set("error_on_missing_placeholder", True)

host = "hexlet.io"

root_path = path.dirname(path.abspath(__file__))
lesson_skeleton_path = path.join(root_path, "data", "skeletons", "lesson")
