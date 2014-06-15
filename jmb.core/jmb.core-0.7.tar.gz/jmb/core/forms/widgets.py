import datetime
import time

from django import forms
from django.contrib.admin import widgets as admin_widgets
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.translation import ugettext as _
from django.utils.datastructures import MultiValueDict
from django.utils.translation import get_language
from django.utils.formats import get_format
from django.utils import datetime_safe, formats

#class DateTimeWidget(admin_widgets.AdminDateWidget):
#    pass

class DatePicker(forms.DateInput):
    class Media:
        js = ("/jsi18n/?app=jmb.core",
		settings.STATIC_URL +'jmb/js/jquery-ui-sliderAccess.js',
		settings.STATIC_URL + "jmb/js/jquery-ui-timepicker-addon.js",)
        css = {
            'all': (settings.STATIC_URL + "jmb/css/jquery-ui-timepicker-addon.css",)
        }
	
    def __init__(self, attrs={}, format=None):
        default_attrs = {'class': 'hasDatePicker'}
        if attrs:
            default_attrs.update(attrs)
        super(DatePicker, self).__init__(attrs=default_attrs, format=format)

class TimePicker(forms.TimeInput):
    class Media:
        js = ("/jsi18n/?app=jmb.core",
		settings.STATIC_URL +'jmb/js/jquery-ui-sliderAccess.js',
		settings.STATIC_URL + "jmb/js/jquery-ui-timepicker-addon.js",)
        css = {
            'all': (settings.STATIC_URL + "jmb/css/jquery-ui-timepicker-addon.css",)
        }
	
    def __init__(self, attrs={}, format=None):
        default_attrs = {'class': 'hasTimePicker','stepMinute':10, 'stepHour':1}
        if attrs:
            default_attrs.update(attrs)
        super(TimePicker, self).__init__(attrs=default_attrs, format=format)

class DateTimePicker(forms.DateTimeInput):
    class Media:
        js = ("/jsi18n/?app=jmb.core",settings.STATIC_URL +'jmb/js/jquery.ui.js',
		settings.STATIC_URL +'jmb/js/jquery-ui-sliderAccess.js',
		settings.STATIC_URL + "jmb/js/jquery-ui-timepicker-addon.js",)
        css = {
            'all': (settings.STATIC_URL + "jmb/css/jquery-ui-timepicker-addon.css",)
        }
	
    def __init__(self, attrs={}, format=None):
        default_attrs = {'class': 'hasDateTimePicker','stepMinute':10, 'stepHour':1}
        if attrs:
            default_attrs.update(attrs)
        super(DateTimePicker, self).__init__(attrs=default_attrs, format=format)

class DateWidget(forms.DateTimeInput):
    class Media:
        js = (settings.STATIC_URL + "js/core.js",
              settings.STATIC_URL + "js/calendar.js",
              settings.STATIC_URL + "js/admin/DateTimeShortcuts.js")

    def __init__(self, attrs={}, format=None):
        super(DateWidget, self).__init__(attrs={'class': 'vDateField', 'size': '10'}, format=format)
        


class DateTimeWidget(forms.SplitDateTimeWidget):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """
    def __init__(self, attrs=None):
        widgets = [DateWidget, admin_widgets.AdminTimeWidget]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return mark_safe(u'<p class="datetime">%s %s<br />%s %s</p>' % \
            (_('Date:'), rendered_widgets[0], _('Time:'), rendered_widgets[1]))
