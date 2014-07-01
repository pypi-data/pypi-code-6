import logging

from django.core.exceptions import ImproperlyConfigured
from django.template.loader import get_template
from django.template import TemplateDoesNotExist, Template

from .base import BaseRenderer

log = logging.getLogger(__name__)

class TemplateRenderer(BaseRenderer):
    '''Base class providing basic functionalities to resolve the template from
       the renderer configuration.
    '''

    @classmethod
    def check_config(cls, config):
        super(TemplateRenderer, cls).check_config(config)
        if not 'template' in config and not 'template_name' in config:
            raise ImproperlyConfigured('{0} configuration is missing a template key: {1!r}'.format(
                    cls.__name__, config))

    def render_template(self):
        '''First try to get a template by path, then compile the inline
           template, and if none of that works show an error message.'''

        if 'template_name' in self.config:
            try:
                return get_template(self.config['template_name'])
            except TemplateDoesNotExist:
                pass
        if 'template' in self.config:
            return Template(self.config['template'])
        log.error('template not found: %r', self.config)
        return 'cmsplugin_blurp/template_not_found.html'
