import operator

import autocomplete_light

from django import forms
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

from models import Checklist, Entry, EntryTag, Map
from utils import tags_string, parse_tags, i18n_fieldnames


class TagsWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        if value is not None and isinstance(value, QuerySet):
            value = tags_string(value)
        return super(TagsWidget, self).render(name, value, attrs)


class StatusField(forms.CharField):
    widget = TagsWidget

    def clean(self, value):
        value = super(StatusField, self).clean(value)
        try:
            values = parse_tags(value)
            if not values:
                return values
            objs = []
            names = i18n_fieldnames('name')
            for value in values:
                try:
                    filters = [Q(**{name: value}) for name in names]
                    objs.append(EntryTag.objects.get(
                        reduce(operator.or_, filters)))
                except EntryTag.DoesNotExist:
                    raise forms.ValidationError(
                        _("EntryTag does not exist: ") + value)
            return objs
        except ValueError:
            raise forms.ValidationError(
                _("Please provide a comma-separated list of tags."))


class EntryInlineAdminForm(forms.ModelForm):
    status = StatusField(label='Status', required=False)

    class Meta:
        model = Entry
        widgets = autocomplete_light.get_widgets_dict(Entry)

    def __init__(self, *args, **kwargs):
        super(EntryInlineAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['status'].initial = self.instance.tags.all()
            self.fields['species'].widget.can_add_related = False

    def save(self, commit=True):
        instance = super(EntryInlineAdminForm, self).save(commit=commit)
        if commit:
            instance.tags.clear()
            for tag in self.cleaned_data.get('status', []):
                instance.tags.add(tag)
        else:
            def save_m2m():
                # function body taken from django/forms/models.py, lines 77-83
                # so any other many-to-many relationships are save. This is
                # added for completeness (future-proofing) though it is not
                # currently used.
                opts = instance._meta
                fields = self.fields
                cleaned_data = self.cleaned_data
                for f in opts.many_to_many:
                    if fields and f.name not in fields:
                        continue
                    if f.name in cleaned_data:
                        f.save_form_data(instance, cleaned_data[f.name])
                # now save the tags, generating from the names entered into
                # the status field.
                instance.tags.clear()
                for tag in cleaned_data.get('status', []):
                    instance.tags.add(tag)
            self.save_m2m = save_m2m
        return instance


class ChecklistForm(forms.ModelForm):

    class Meta:
        model = Checklist
        widgets = autocomplete_light.get_widgets_dict(Checklist)


class MapForm(autocomplete_light.GenericModelForm):
    content_object = autocomplete_light.GenericModelChoiceField(
        widget=autocomplete_light.ChoiceWidget(
            autocomplete='AutocompleteMap',
            autocomplete_js_attributes={'minimum_characters': 0}))

    class Meta:
        model = Map
