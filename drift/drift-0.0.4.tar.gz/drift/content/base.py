'''
System to registring behaviour classes with the content
management system. Class should extent ModelContent.
'''
import inspect
from django.conf import settings
from django.db import models
from django.db.models.base import ModelBase, Model
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django import forms
from django.forms.models import modelform_factory
from django.utils.encoding import force_text, smart_text
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe

from drift import widgets as content_widgets
from drift.forms import BootstrapForm
from .editor import DriftBootstrapWYSIWYGEditor


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class ContentForm(object):
    def __init__(self, form, content):
        self.form = form
        self.content = content

    def __iter__(self):
        for field in self.form:
            yield ContentField(self.form, field)

    def __getitem__(self, name):
        return self.form[name]

    @property
    def non_contenteditable_fields(self):
        for field in self.form:
            if field.name in self.content.contenteditable:
                continue
            yield ContentField(self.form, field)

    def non_field_errors(self):
        return self.form.non_field_errors()


class ContentField(object):
    def __init__(self, form, field):
        self.field = field # A django.forms.BoundField instance
        self.is_checkbox = isinstance(self.field.field.widget, forms.CheckboxInput)

    def label_tag(self):
        classes = []
        contents = conditional_escape(force_text(self.field.label))
        if self.is_checkbox:
            classes.append('checkbox')

        if self.field.field.required:
            classes.append('required')
        attrs = {'class': ' '.join(classes)} if classes else {}
        # checkboxes should not have a label suffix as the checkbox appears
        # to the left of the label.
        return self.field.label_tag(contents=mark_safe(contents), attrs=attrs)

    def checkbox_field(self):
        classes = []
        contents = conditional_escape(force_text(self.field.label))
        if self.is_checkbox:
            classes.append('checkbox')

        if self.field.field.required:
            classes.append('required')
        attrs = {'class': ' '.join(classes)} if classes else {}
        # checkboxes should not have a label suffix as the checkbox appears
        # to the left of the label.

        contents = force_text(self.field) + contents

        return self.field.label_tag(contents=mark_safe(contents), attrs=attrs)



    def errors(self):
        return mark_safe(self.field.errors.as_ul())


class BootstrappedModelForm(BootstrapForm, forms.ModelForm):
    pass

class ModelContent(object):
    name = "Content"
    exclude = None
    panels = ()
    contenteditable = ()
    widgets = {}
    prepopulated_fields = {}

    menu = (
        ("New", "get_new_url"),
        ("-", None),
        ("Admin", "get_admin_url"),
    )

    _form = None
    _content_form = None

    def __init__(self, instance, model_class, request, system, editor_class=None):
        '''
        Note instance can be None
        '''
        self.instance = instance
        self.model_class = model_class
        self.system = system
        self.editor = self.get_editor(editor_class)

        self.get_form(initial=self.get_form_initial_data(request)) # get the default form

    @property
    def form(self):
        '''
        Convenient for templates, but will be None
        unless get_form called first.
        '''
        if self._form is None:
            return None
        if self._content_form is None:
            self._content_form = ContentForm(self._form, self)
        return self._content_form

    def get_form_initial_data(self, request):
        return None
     
    def get_form(self, data=None, *args, **kwargs):
        self._form = modelform_factory(
            self.model_class,
            form=BootstrappedModelForm,
            exclude=self.exclude,
            formfield_callback = self.formfield_for_dbfield
        )(data, *args, instance=self.instance, **kwargs)
        return self._form

    def get_editor(self, editor_class):

        if editor_class is not None:
            return editor_class()

        settings_editor = getattr(settings, 'DRIFT_EDITOR_CLASS', None)
        if settings_editor is None:
            return DriftBootstrapWYSIWYGEditor()

        module, classname = settings_editor.rsplit('.', 1)
        mod = __import__(module, fromlist=[classname])
        editor_class = getattr(mod, classname)
        return editor_class()

    @property
    def get_panels(self):
        return [class_() for class_ in self.panels]

    @property
    def get_perpopulated_fields(self):
        '''
        return prepopulated fields formatted as a javascript list.
        '''
        ret = []
        if self.form is not None:
            for key in self.prepopulated_fields:
                target_field = self.form[key]
                source_field = self.form[self.prepopulated_fields[key]]
                ret.append(
                    "{{target_id: '{0}', source_id: '{1}'}}".format(
                        target_field.auto_id,
                        source_field.auto_id,
                    )
                )
        return mark_safe('[{0}]'.format(', '.join(ret)))

    def formfield_for_dbfield(self, dbfield, **kwargs):
        # User override
        if dbfield.name in self.widgets:
            kwargs = dict(widget=self.widgets[dbfield.name], **kwargs)
            return dbfield.formfield(**kwargs)

        # Overrides for all widgets
        if isinstance(dbfield, models.DateField):
            kwargs = dict(widget=content_widgets.ContentDateInput, **kwargs)
            return dbfield.formfield(**kwargs)

        # Content system overrides
        if dbfield.name in self.contenteditable:
            if isinstance(dbfield, models.CharField):
                kwargs = dict(widget=content_widgets.ContentEditableTextInput, **kwargs)
                return dbfield.formfield(**kwargs)
            elif isinstance(dbfield, models.TextField):
                kwargs = dict(widget=self.editor.get_textarea_widget(), **kwargs)
                return dbfield.formfield(**kwargs)

        return dbfield.formfield(**kwargs)

    def get_new_url(self):
        raise NotImplementedError

    def get_admin_url(self):
        # TODO: pass in the request into the content object and
        # then return non if user isn't staff...
        if self.instance is None:
            view_name = "admin:{0}_{1}_changelist".format(
                self.model_class._meta.app_label,
                self.model_class.__name__.lower(),
            )
            return reverse_lazy(view_name)
        else:
            view_name = "admin:{0}_{1}_change".format(
                self.model_class._meta.app_label,
                self.model_class.__name__.lower(),
            )
            return reverse_lazy(view_name, args=(self.instance.pk,))

    def check_can_view(self, request):
        '''
        Check if the requestor can view the content. If
        it can't, Http404 will be raised
        '''
        if self.is_published():
            return True
        else:
            if request.user.is_authenticated():
                # More restrictive option would be to required
                # the logged in user have the can_change permission
                return True

            else:
                raise Http404

    def check_can_edit(self, request):
        if not self.can_edit(request):
            raise PermissionDenied

    def can_edit(self, request):
        '''
        Returns True is requestor can edit, else False.
        The caller will have to respond with 403 or whatever
        makes sense in their situtation.
        '''
        if request.user.is_authenticated():
            options = self.model_class._meta
            permission = '{}.change_{}'.format(options.app_label, self.model_class.__name__.lower())
            return request.user.has_perm(permission)
        else:
            return False

    def check_can_add(self, request):
        if not self.can_add(request):
            raise PermissionDenied

    def can_add(self, request):
        '''
        Returns True is requestor can add, else False.
        The caller will have to respond with 403 or whatever
        makes sense in their situtation.
        '''
        if request.user.is_authenticated():
            options = self.model_class._meta
            permission = '{}.add_{}'.format(options.app_label, self.model_class.__name__.lower())
            return request.user.has_perm(permission)
        else:
            return False

    def get_edit_url(self):
        raise NotImplementedError

    def get_publish_url(self):
        raise NotImplementedError

    def is_published(self):
        return True

    def get_version(self):
        return None

    def get_created(self):
        if self.instance is not None:
            if hasattr(self.instance, 'created'):
                return self.instance.created
        return None

    def get_owner(self):
        return None

    @property
    def non_contenteditable_fields(self):
        if self.instance is None:
            return

        for field in self._form:
            if field.name in self.contenteditable:
                continue
            yield field

    def get_menu(self):
        '''
        process the menu variable and return name, href for each link
        '''
        for name, link_string in self.menu:
            if link_string is None:
                yield name, link_string
                continue
            attr = getattr(self, link_string, None)
            if attr is not None:
                if callable(attr):
                    link = attr()
                else:
                    link = attr
            else:
                link = link_string
            yield name, link


class ContentPanelBase(object):
    def get_header(self):
        '''
        Oppertunity to insert buttons or other controls into the header.
        Return valid HTML
        '''
        raise NotImplementedError

    def get_panel_template_name(self):
        '''
        Return the name of template to be included into the content UI.
        '''
        raise NotImplementedError


class ContentSystem(object):
    '''
    The ContentSystem object encapsulates the state of the
    behaviour of the content system. The key function is to
    assoicate ModelContent object with given models.
    '''
    def __init__(self):
        self._registry = {} # model -> model content class

    def register(self, model_or_iterable, content_class=None):
        '''
        Similar to the admin system register function.
        Assoicates the given model or models with the provided
        content_class constructed with the model.
        '''
        if content_class is None:
            content_class = ModelContent

        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]

        for model in model_or_iterable:
            if model._meta.abstract:
                raise ImproperlyConfigured(
                    'The model {0} is abstract, so it '
                    'cannot be registered with admin.'.format(model.__name__)
                )

            if model in self._registry:
                raise AlreadyRegistered(
                    'The model {0} is already registered. '
                    'Use unregister() first to override'.format(model.__name__)
                )

            # I don't fully know how models get swapped, --AOC
            if not model._meta.swapped:
                self._registry[model] = content_class


    def unregister(self, model_or_iterable):
        '''
        Unregisters the given model(s).

        If a model isn't already registered, this will raise NotRegistered.
        '''
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]

        for model in model_or_iterable:
            if model not in self._registry:
                raise NotRegistered(
                    'The model {0} is not registered'.format(model.__name__)
                )
            del self._registry[model]


    def get_content_class(self, model):
        return self._registry[model]


# Global system object for the common base, you could create your own...
system = ContentSystem()


def make_content(instance_or_model, request=None, action='view', content_system=None):
    '''
    Wrap a instance of a content object with the
    content class it has registered, if it doesn't
    have one registered wrap it with the default class.

    return render(
        request,
        template,
        dict(content=make_content(instance))
    )

    Then in the template {{ content }} give access to the
    content object and {{ content.instance }} give access
    to the instance of the content.

    If a request/action is provided permission checking is done
    and Http404 or PermissionDeined can be raised.
    '''
    if content_system is None:
        global system
        content_system = system

    if inspect.isclass(instance_or_model):
        model = instance_or_model
        instance = None
    else:
        instance = instance_or_model
        if not isinstance(instance, Model):
            raise ValueError(
                'instance must be a Django model, ie derived from ModelBase'
            )
        model = instance.__class__

    content_class = content_system.get_content_class(model)
    content_obj =  content_class(
        instance,
        model,
        request,
        content_system,
    )

    if request is not None:
        if action == 'view':
            content_obj.check_can_view(request)
        elif action == 'edit':
            content_obj.check_can_edit(request)
        elif action == 'create':
            content_obj.check_can_add(request)
        else:
            raise ValueError('{} is not a valid action'.format(action))

    return content_obj
