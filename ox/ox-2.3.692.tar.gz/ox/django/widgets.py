import django.newforms as forms
from string import Template
from django.utils.safestring import mark_safe

class FirefoggWidget(forms.FileInput):
  def render(self, name, value, attrs=None):
    tpl = Template(u"""<h1>This should be a Firefogg widget for $name, current value: $value</h1>""")
    return mark_safe(tpl.substitute(name=name, value=value))

