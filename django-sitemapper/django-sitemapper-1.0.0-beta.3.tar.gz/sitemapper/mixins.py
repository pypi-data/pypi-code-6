import warnings
warnings.warn(
    "'sitemapper.mixins.Sitemap' is deprecated, and will be removed in"
    " future versions; use 'sitemapper.sitemaps.Sitemap' instead.",
    DeprecationWarning
    )

from sitemapper.sitemaps import Sitemap  # noqa
