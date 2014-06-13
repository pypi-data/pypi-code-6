import logging
import mimetypes
from grow.common import utils
from grow.pods import errors
from grow.pods.controllers import base
from grow.pods.controllers import tags
from grow.pods.storage import gettext_storage as gettext


class PageController(base.BaseController):

  KIND = 'Page'

  class Defaults(object):
    LL = 'en'
    LOCALE = None
    CC = None

  def __init__(self, view=None, document=None, path=None, _pod=None):
    self.view = view
    self.document = document
    self.path = path
    super(PageController, self).__init__(_pod=_pod)

  def __repr__(self):
    if not self.document:
      return '<Page(view=\'{}\')>'.format(self.view)
    return '<Page(view=\'{}\', document=\'{}\')>'.format(self.view, self.document.pod_path)

  @property
  def mimetype(self):
    return mimetypes.guess_type(self.view)[0]

  @property
  def locale(self):
    if self.document:
      return self.document.locale

  @property
  def ll(self):
    return self.route_params.get('ll', PageController.Defaults.LL)

  @property
  def cc(self):
    return self.route_params.get('cc', PageController.Defaults.CC)

  @property
  @utils.memoize
  def _template_env(self):
    return self.pod.get_template_env()

  def _install_translations(self, ll):
    if ll is None:
      gettext_translations = gettext.NullTranslations()
    else:
      translation = self.pod.translations.get_translation(ll)
      gettext_translations = translation.get_gettext_translations()
    self._template_env.uninstall_gettext_translations(None)
    self._template_env.install_gettext_translations(gettext_translations, newstyle=True)

  def list_concrete_paths(self):
    if self.path:
      return [self.path]
    if not self.document:
      raise
    return [self.document.get_serving_path()]

  def render(self):
    # TODO(jeremydw): This is a bit hacky. Be more explicit about translations.
    ll = self.locale
    self._install_translations(ll)
    template = self._template_env.get_template(self.view.lstrip('/'))
    context = {}
    context = {
        'categories': lambda *args, **kwargs: tags.categories(*args, _pod=self.pod, **kwargs),
        'docs': lambda *args, **kwargs: tags.docs(*args, _pod=self.pod, **kwargs),
        'doc': lambda *args, **kwargs: tags.get_doc(*args, _pod=self.pod, **kwargs),
        'static': lambda path: tags.static(path, _pod=self.pod),
        'breadcrumb': lambda *args, **kwargs: tags.breadcrumb(*args, _pod=self.pod, **kwargs),
        'nav': lambda *args, **kwargs: tags.nav(*args, _pod=self.pod, **kwargs),
        'cc': self.cc,
        'll': self.ll,
        'params': self.route_params,
        'pod': self.pod,
        'url': lambda *args, **kwargs: tags.url(*args, _pod=self.pod, **kwargs),
    }
    try:
      return template.render({
          'g': context,
          'doc': self.document,
          'podspec': self.pod.get_podspec(),
      })
    except Exception as e:
      text = 'Error building {}: {}'
      logging.exception(e)
      raise errors.BuildError(text.format(self, e))
