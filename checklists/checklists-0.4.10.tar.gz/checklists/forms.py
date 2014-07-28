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

    def save(self, commit=True):
        instance = super(EntryInlineAdminForm, self).save(commit=commit)
        instance.tags.clear()
        for tag in self.cleaned_data.get('status', []):
            instance.tags.add(tag)
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
