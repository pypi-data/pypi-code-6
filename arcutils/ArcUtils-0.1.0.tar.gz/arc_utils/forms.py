import types
from django.forms.widgets import RadioSelect
from django.forms.forms import BoundField, Form
from django import forms
from django.db import models
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxInput, ClearableFileInput, DateInput, CheckboxSelectMultiple
from django.forms.util import ErrorList
from django.utils.html import format_html, format_html_join
from django.utils.encoding import force_text

class BootstrapFormWrapper(object):
    def __getitem__(self, name):
        """
        Add some useful attributes to the boundfield objects
        """
        bound_field = super(BootstrapFormWrapper, self).__getitem__(name)
        if isinstance(bound_field.field.widget, CheckboxInput):
            bound_field.is_checkbox = True
        if isinstance(bound_field.field.widget, DateInput):
            bound_field.is_date = True
        if isinstance(bound_field.field.widget, CheckboxSelectMultiple):
            bound_field.is_multi_checkbox = True

        classes = bound_field.field.widget.attrs.get("class", "")
        if isinstance(bound_field.field.widget, (forms.widgets.TextInput, forms.widgets.Textarea)):
            bound_field.field.widget.attrs['class'] = classes + " form-control"
        return bound_field

class BootstrapForm(BootstrapFormWrapper, Form):
    pass

class BootstrapModelForm(BootstrapFormWrapper, ModelForm):
    pass

forms.Form = BootstrapForm
forms.ModelForm = BootstrapModelForm

# monkey patch the ClearableFileInput so it looks better
ClearableFileInput.initial_text = 'Currently'
ClearableFileInput.input_text = 'Change'
ClearableFileInput.clear_checkbox_label = 'Clear'
ClearableFileInput.template_with_initial = '%(initial_text)s: %(initial)s %(clear_template)s %(input_text)s: %(input)s'
ClearableFileInput.template_with_clear = '<label class="clear-label" for="%(clear_checkbox_id)s">%(clear)s %(clear_checkbox_label)s</label><br />'

# monkey patch the ErrorList so it has a bootstrap css class (text-danger)
ErrorList.as_ul = lambda self: '' if not self else format_html('<ul class="errorlist text-danger">{0}</ul>', format_html_join('', '<li>{0}</li>', ((force_text(e),) for e in self)))

# monkey patch BoundFields so that it has an error_class attribute that returns
# "has-error" or the empty string
BoundField.error_class = lambda self: "has-error" if self.errors else ""

class CustomDatePickerInput(DateTimePicker):    
    ''' sets up default options for our datepickers '''
    def __init__(self, attrs=None, format=None, options=None, div_attrs=None, icon_attrs=None):
        if options == None: options = dict()
    # define our custom options here:
    options['pickTime'] = False   
    options['format'] = 'MM/DD/YYYY'

    super(CustomDatePickerInput, self).__init__(attrs, format, options, div_attrs, icon_attrs)

class CustomDateTimePickerInput(DateTimePicker):
    ''' sets up default options for our datetimepickers '''
    def __init__(self, attrs=None, format=None, options=None, div_attrs=None, icon_attrs=None):
        if options == None: options = dict()
    # define our custom options here:
    options['sideBySide'] = True        # FIXME: doesn't seem to work properly.
    options['format'] = 'MM/DD/YYYY HH:mm'

    super(CustomDateTimePickerInput, self).__init__(attrs, format, options, div_attrs, icon_attrs)

class RadioSelectWithBetterSubwidgets(RadioSelect):
    """
    This class overrides the subwidgets method, so that it provides the
    subwidget, and the choice value that the subwidget represents
    """
    def subwidgets(self, name, value, attrs=None, choices=()):
        # the normal subwidgets method only returns the widget, but we also want the choice value
    for widget, choice in zip(self.get_renderer(name, value, attrs, choices), self.choices):
        yield widget, choice[0]


class CustomForm(Form):
    def __init__(self, *args, **kwargs):
        super(CustomForm, self).__init__(*args, **kwargs)

    def _add_error(self, field_name, error):
        self._errors.setdefault(field_name, self.error_class()).append(error)
        self.cleaned_data.pop(field_name, None)

    def __iter__(self):
        for bound_field in super(CustomForm, self).__iter__():
            if isinstance(bound_field.field.widget, CheckboxInput):
                bound_field.is_checkbox = True
            if isinstance(bound_field.field.widget, DateInput):
                bound_field.is_date = True
            yield bound_field


class CustomModelForm(ModelForm):
    def __init__(self, *args, **kwargs):

        super(CustomModelForm, self).__init__(*args, **kwargs)

    def __iter__(self):
        for bound_field in super(CustomModelForm, self).__iter__():
            if isinstance(bound_field.field.widget, CheckboxInput):
                bound_field.is_checkbox = True
            if isinstance(bound_field.field.widget, DateInput):
                bound_field.is_date = True
            yield bound_field

    def _add_error(self, field_name, error):
        self._errors.setdefault(field_name, self.error_class()).append(error)
        self.cleaned_data.pop(field_name, None)


class FilterForm(CustomForm):
    """
    Handles filtering of list views. Subclasses should override the items() method
    """

    @property
    def values(self):
        """
        This returns a dict with the initial data on the form, and any possible
        cleaned data values. If a field has an initial value and a
        cleaned_data, the cleaned_data has precedence 
        """
        if not hasattr(self, "_values"):
            self._values = self._merge_initial_and_cleaned_data()
        return self._values

    def items(self):
        """
        Subclasses should override this and return an iterable of items that
        match the criteria in the self.values dict
        """
        return []

    def _merge_initial_and_cleaned_data(self):
        if self.is_bound:
            # populate the cleaned_data attribute
            self.is_valid()
        else:
            self.cleaned_data = {}

        # combine the cleaned_data with the initial data
        initial = dict((k, self.initial.get(k, field.initial)) for k, field in self.fields.items())
        return dict(initial.items() + self.cleaned_data.items())

