import django
from django.conf import settings
from django.template import loader, Context

def app_flag(input):
    def output(request, *args, **kwargs):
        data = input(request, *args, **kwargs)
        if data.content:
            try:
                t = loader.get_template(settings.DJANGO_APP_FLAG_TEMPLATE)
            except Exception as e:
                t = loader.get_template('djangoAppFlagTemplate.html')
            c = Context({'version': _version()})
            html = t.render(c)
            data.content += html
        return data
    output.__name__ = input.__name__
    output.__dict__ = input.__dict__
    output.__doc__ = input.__doc__
    return output

def _version():
    return '.'.join([str(v) for v in list(django.VERSION)[0:3]])
