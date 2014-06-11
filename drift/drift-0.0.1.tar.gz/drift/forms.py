from django import forms

from django import forms
from django.template import Template, Context


boostrap_template = '''
{% if form.non_field_errors %}
<div class="form_errors">
{% for error in form.non_field_errors %}
<div class="error">{{ error }}</div>
{% endfor %}
{% endif %}
{% for field in form.visible_fields %}
<div class="form-group">
  <label for="{{ field.html_name }}" class="control-label{% if field.field.required %} required{% endif %}">{{ field.label }}</label>
  <div class="controls">
    {{ field }}
    {% if field.errors %}
    <div class="field_errors">
          {{ field.errors }}
    </div>
    {% endif %}
    {% if field.help_text %}
    <span class="help-block">{{ field.help_text }}</span>
    {% endif %}
  </div>
</div>
{% endfor %}
{% for field in form.hidden_fields %}
{{ field }}
{% endfor %}
'''


horizontal_template = '''
{% if form.non_field_errors %}
<div class="form_errors">
{% for error in form.non_field_errors %}
<div class="error">{{ error }}</div>
{% endfor %}
{% endif %}
{% for field in form.visible_fields %}
<div class="form-group">
  <label for="{{ field.html_name }}" class="control-label{% if field.field.required %} required{% endif %}">{{ field.label }}</label>
  <div class="controls">
    {{ field }}
    {% if field.errors %}
    <div class="field_errors">
          {{ field.errors }}
    </div>
    {% endif %}
    {% if field.help_text %}
    <span class="help-block">{{ field.help_text }}</span>
    {% endif %}
  </div>
</div>
{% endfor %}
{% for field in form.hidden_fields %}
{{ field }}
{% endfor %}
'''


# Mixin
class BootstrapForm(object):
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            field = self.fields[field]
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                continue
            classes = ['form-control']
            if 'class' in field.widget.attrs:
                classes.append(field.widget.attrs['class'])
            field.widget.attrs.update(
                {'class' : ' '.join(classes)}
            )

    def as_bootstrap_horizontal(self):
        template = Template(horizontal_template)
        ctx = Context(dict(form=self))
        return template.render(ctx)

    def as_bootstrap(self):
        template = Template(bootstrap_template)
        ctx = Context(dict(form=self))
        return template.render(ctx)
