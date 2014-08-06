from os.path import join
from pkg_resources import resource_string

from django.template import loader
from django.template.base import TemplateDoesNotExist

class EggAppLoader(loader.BaseLoader):
    '''
    This loader is similar to the builtin django egg loader
    except that it takes the following format:

    <appname>/<template_name> 
    looks at 
    <appname>/templates/<template_name>

    '''
    is_usable =  resource_string is not None

    def load_template_source(self, template_name, template_dirs=None):
        app = template_name.split("/")[0]
        resource_path = "templates/%s" % join(*template_name.split("/")[1:])
        try:
            resource = resource_string(app, resource_path)
        except Exception:
            raise TemplateDoesNotExist, template_name
        return (resource, 'egg:%s:%s' % (app, resource_path))
