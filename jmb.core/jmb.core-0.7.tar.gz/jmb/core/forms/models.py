# -*- coding: utf-8 -*-
import re
from datetime import date, datetime
from functools import partial, reduce, update_wrapper

from django.contrib import admin
from django import forms, template
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.admin.util import unquote
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.admin import helpers

from jmb.core.forms.widgets import DateWidget, DateTimeWidget
from jmb.core.middleware.thread_local import get_request

class ModelForm(forms.ModelForm):
    def __init__(self, *args, **kws):
        super(ModelForm, self).__init__(*args, **kws)
        if self.fields.has_key('date_create'):
            self.fields.pop('date_create')

        if self.fields.has_key('date_last_modify'):
            self.fields.pop('date_last_modify')

        if self.fields.has_key('status'):
            self.fields['status'].required = False


class AdminModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminModelForm, self).__init__(*args, **kwargs)
        try:
            self.fields['date_create'].required = False
            self.fields['date_last_modify'].required = False
        except:
            pass
        try:
            self.fields['creator'].required = False
            self.fields['last_modifier'].required = False
        except:
            pass
        try:
            self.fields['ordering'].required = False
        except:
            pass

    def get_object_id(self, obj):
        if not self.instance or not self.instance.id:
            if self.data:
                #form di ADD in errore
                if self.data.get(obj): return self.data[obj]
            if self.initial:
                #form di ADD iniziale
                if self.initial.get(obj): return self.initial[obj]
            return None
        else:
            if not self.data:
                #form di EDIT
                if getattr(self.instance, obj, None): return getattr(self.instance, obj).id
                else: return None
            else:
                #form di EDIT in errore
                if self.data.get(obj): return self.data[obj]
                else: return None
