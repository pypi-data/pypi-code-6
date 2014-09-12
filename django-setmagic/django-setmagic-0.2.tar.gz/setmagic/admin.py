from django import forms
from django.contrib import admin
from django.utils.importlib import import_module

from setmagic import settings
from setmagic.models import Setting


_denied = lambda *args: False


class SetMagicAdmin(admin.ModelAdmin):
    list_display = ('label', 'current_value',)
    list_editable = ('current_value',)
    list_display_links = ()

    has_add_permission = _denied
    has_delete_permission = _denied

    # Make all fields read-only at the change form
    def get_readonly_fields(self, *args, **kwargs):
        return self.opts.get_all_field_names()

    def changelist_view(self, *args, **kwargs):
        settings._sync()
        return super(SetMagicAdmin, self).changelist_view(*args, **kwargs)

    def get_queryset(self, request):
        return Setting.objects.filter(name__in=settings.defs)

    def get_changelist_form(self, *args, **kwargs):
        class Form(forms.ModelForm):

            class Meta:
                fields = self.list_editable

            def __init__(self, *args, **kwargs):
                super(Form, self).__init__(*args, **kwargs)

                # Do nothing for empty forms
                if not self.instance.pk:
                    return

                # Set a custom field
                custom_field = settings.defs[self.instance.name].get('field')
                if custom_field:
                    if isinstance(custom_field, str):
                        module, name = custom_field.rsplit('.', 1)
                        custom_field = getattr(import_module(module), name)()
                    self.fields['current_value'] = custom_field
                else:
                    self.fields['current_value'] = forms.CharField()

                # Make the field non-required
                self.fields['current_value'].required = False

        return Form

admin.site.register(Setting, SetMagicAdmin)
