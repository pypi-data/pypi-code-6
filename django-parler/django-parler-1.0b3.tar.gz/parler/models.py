"""
Simple but effective translation support.

Integrating *django-hvad* (v0.3) in advanced projects turned out to be really hard,
as it changes the behavior of the QuerySet iterator, manager methods
and model metaclass which *django-polymorphic* and friends also rely on.
The following is a "crude, but effective" way to introduce multilingual support.

Added on top of that, the API-suger is provided, similar to what django-hvad has.
It's possible to create the translations model manually,
or let it be created dynamically when using the :class:`TranslatedFields` field.
"""
from __future__ import unicode_literals
import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models, router
from django.db.models.base import ModelBase
from django.db.models.fields.related import ReverseSingleRelatedObjectDescriptor
from django.utils.functional import lazy
from django.utils.translation import get_language, ugettext, ugettext_lazy as _
from django.utils import six
from parler import signals
from parler.cache import _cache_translation, _cache_translation_needs_fallback, _delete_cached_translation, get_cached_translation, _delete_cached_translations, get_cached_translated_field
from parler.fields import TranslatedField, LanguageCodeDescriptor, TranslatedFieldDescriptor
from parler.managers import TranslatableManager
from parler.utils.i18n import normalize_language_code, get_language_settings, get_language_title
import sys
import logging

logger = logging.getLogger(__name__)



class TranslationDoesNotExist(AttributeError):
    """
    A tagging interface to detect missing translations.
    The exception inherits from :class:`AttributeError` to reflect what is actually happening.
    It also causes the templates to handle the missing attributes silently, which is very useful in the admin for example.
    """
    pass


_lazy_verbose_name = lazy(lambda x: ugettext("{0} Translation").format(x._meta.verbose_name), six.text_type)


def create_translations_model(shared_model, related_name, meta, **fields):
    """
    Dynamically create the translations model.
    Create the translations model for the shared model 'model'.

    :param related_name: The related name for the reverse FK from the translations model.
    :param meta: A (optional) dictionary of attributes for the translations model's inner Meta class.
    :param fields: A dictionary of fields to put on the translations model.

    Two fields are enforced on the translations model:

        language_code: A 15 char, db indexed field.
        master: A ForeignKey back to the shared model.

    Those two fields are unique together.
    """
    if not meta:
        meta = {}

    # Define inner Meta class
    meta['unique_together'] = list(meta.get('unique_together', [])) + [('language_code', 'master')]
    meta['app_label'] = shared_model._meta.app_label
    meta.setdefault('db_table', shared_model._meta.db_table + '_translation')
    meta.setdefault('verbose_name', _lazy_verbose_name(shared_model))

    # Define attributes for translation table
    name = str('{0}Translation'.format(shared_model.__name__))  # makes it bytes, for type()

    attrs = {}
    attrs.update(fields)
    attrs['Meta'] = type(str('Meta'), (object,), meta)
    attrs['__module__'] = shared_model.__module__
    attrs['objects'] = models.Manager()
    attrs['master'] = models.ForeignKey(shared_model, related_name=related_name, editable=False, null=True)

    # Create and return the new model
    translations_model = TranslatedFieldsModelBase(name, (TranslatedFieldsModel,), attrs)

    # Register it as a global in the shared model's module.
    # This is needed so that Translation model instances, and objects which refer to them, can be properly pickled and unpickled.
    # The Django session and caching frameworks, in particular, depend on this behaviour.
    mod = sys.modules[shared_model.__module__]
    setattr(mod, name, translations_model)

    return translations_model


class TranslatedFields(object):
    """
    Wrapper class to define translated fields on a model.

    The field name becomes the related name of the :class:`TranslatedFieldsModel` subclass.

    Example::
        from django.db import models
        from parler.models import TranslatableModel, TranslatedFields

        class MyModel(TranslatableModel):
            translations = TranslatedFields(
                title = models.CharField("Title", max_length=200)
            )
    """
    def __init__(self, meta=None, **fields):
        self.fields = fields
        self.meta = meta
        self.name = None

    def contribute_to_class(self, cls, name):
        self.name = name

        # Called from django.db.models.base.ModelBase.__new__
        translations_model = create_translations_model(cls, name, self.meta, **self.fields)

        # The metaclass (TranslatedFieldsModelBase) should configure this already:
        assert cls._translations_model == translations_model
        assert cls._translations_field == name



class TranslatableModel(models.Model):
    """
    Base model class to handle translations.
    """

    # Consider these fields "protected" or "internal" attributes.
    # Not part of the public API, but used internally in the class hierarchy.
    _translations_field = None
    _translations_model = None

    language_code = LanguageCodeDescriptor()

    # change the default manager to the translation manager
    objects = TranslatableManager()

    class Meta:
        abstract = True


    def __init__(self, *args, **kwargs):
        # Still allow to pass the translated fields (e.g. title=...) to this function.
        translated_kwargs = {}
        current_language = None
        if kwargs:
            current_language = kwargs.pop('_current_language', None)
            for field in self._translations_model.get_translated_fields():
                try:
                    translated_kwargs[field] = kwargs.pop(field)
                except KeyError:
                    pass

        # Run original Django model __init__
        super(TranslatableModel, self).__init__(*args, **kwargs)

        self._translations_cache = {}
        self._current_language = normalize_language_code(current_language or get_language())  # What you used to fetch the object is what you get.

        # Assign translated args manually.
        if translated_kwargs:
            translation = self._get_translated_model(auto_create=True)
            for field, value in six.iteritems(translated_kwargs):
                setattr(translation, field, value)


    def get_current_language(self):
        """
        Get the current language.
        """
        # not a property, so won't conflict with model fields.
        return self._current_language


    def set_current_language(self, language_code, initialize=False):
        """
        Switch the currently activate language of the object.
        """
        self._current_language = normalize_language_code(language_code or get_language())

        # Ensure the translation is present for __get__ queries.
        if initialize:
            self._get_translated_model(use_fallback=False, auto_create=True)


    def get_fallback_language(self):
        """
        Return the fallback language code,
        which is used in case there is no translation for the currently active language.
        """
        lang_dict = get_language_settings(self._current_language)
        return lang_dict['fallback'] if lang_dict['fallback'] != self._current_language else None


    def has_translation(self, language_code=None):
        """
        Return whether a translation for the given language exists.
        Defaults to the current language code.
        """
        if language_code is None:
            language_code = self._current_language

        try:
            # Check the local cache directly, and the answer is known.
            # NOTE this may also return newly auto created translations which are not saved yet.
            return self._translations_cache[language_code] is not None
        except KeyError:
            try:
                # Fetch from DB, fill the cache.
                self._get_translated_model(language_code, use_fallback=False, auto_create=False)
            except self._translations_model.DoesNotExist:
                return False
            else:
                return True


    def get_available_languages(self):
        """
        Return the language codes of all translated variations.
        """
        qs = self._get_translated_queryset()
        if qs._prefetch_done:
            return sorted(obj.language_code for obj in qs)
        else:
            return qs.values_list('language_code', flat=True).order_by('language_code')


    def _get_translated_model(self, language_code=None, use_fallback=False, auto_create=False):
        """
        Fetch the translated fields model.
        """
        if not self._translations_model or not self._translations_field:
            raise ImproperlyConfigured("No translation is assigned to the current model!")

        if not language_code:
            language_code = self._current_language

        # 1. fetch the object from the local cache
        try:
            object = self._translations_cache[language_code]

            # If cached object indicates the language doesn't exist, need to query the fallback.
            if object is not None:
                return object
        except KeyError:
            # 2. No cache, need to query
            # Check that this object already exists, would be pointless otherwise to check for a translation.
            if not self._state.adding and self.pk:
                qs = self._get_translated_queryset()
                if qs._prefetch_done:
                    # 2.1, use prefetched data
                    # If the object is not found in the prefetched data (which contains all translations),
                    # it's pointless to check for memcached (2.2) or perform a single query (2.3)
                    for object in qs:
                        if object.language_code == language_code:
                            self._translations_cache[language_code] = object
                            _cache_translation(object)  # Store in memcached
                            return object
                else:
                    # 2.2, fetch from memcached
                    object = get_cached_translation(self, language_code, use_fallback=use_fallback)
                    if object is not None:
                        # Track in local cache
                        if object.language_code != language_code:
                            self._translations_cache[language_code] = None  # Set fallback marker
                        self._translations_cache[object.language_code] = object
                        return object
                    else:
                        # 2.3, fetch from database
                        try:
                            object = qs.get(language_code=language_code)
                        except self._translations_model.DoesNotExist:
                            pass
                        else:
                            self._translations_cache[language_code] = object
                            _cache_translation(object)  # Store in memcached
                            return object

        # Not in cache, or default.
        # Not fetched from DB

        # 3. Auto create?
        if auto_create:
            # Auto create policy first (e.g. a __set__ call)
            object = self._translations_model(
                language_code=language_code,
                master=self  # ID might be None at this point
            )
            self._translations_cache[language_code] = object
            # Not stored in memcached here yet, first fill + save it.
            return object

        # 4. Fallback?
        fallback_msg = None
        lang_dict = get_language_settings(language_code)

        if use_fallback and (lang_dict['fallback'] != language_code):
            # Explicitly set a marker for the fact that this translation uses the fallback instead.
            # Avoid making that query again.
            self._translations_cache[language_code] = None  # None value is the marker.
            if not self._state.adding or self.pk:
                _cache_translation_needs_fallback(self, language_code)

            # Jump to fallback language, return directly.
            # Don't cache under this language_code
            try:
                return self._get_translated_model(lang_dict['fallback'], use_fallback=False, auto_create=auto_create)
            except self._translations_model.DoesNotExist:
                fallback_msg = " (tried fallback {0})".format(lang_dict['fallback'])

        # None of the above, bail out!
        raise self._translations_model.DoesNotExist(
            "{0} does not have a translation for the current language!\n"
            "{0} ID #{1}, language={2}{3}".format(self._meta.verbose_name, self.pk, language_code, fallback_msg or ''
        ))


    def _get_any_translated_model(self):
        """
        Return any available translation.
        Returns None if there are no translations at all.
        """
        if self._translations_cache:
            # There is already a language available in the case. No need for queries.
            # Give consistent answers if they exist.
            try:
                return self._translations_cache.get(self._current_language, None) \
                    or self._translations_cache.get(self.get_fallback_language(), None) \
                    or next(t for t in six.itervalues(self._translations_cache) if t if not None)  # Skip fallback markers.
            except StopIteration:
                pass

        try:
            # Use prefetch if available, otherwise perform separate query.
            qs = self._get_translated_queryset()
            if qs._prefetch_done:
                translation = list(qs)[0]
            else:
                translation = qs[0]
        except IndexError:
            return None
        else:
            self._translations_cache[translation.language_code] = translation
            _cache_translation(translation)
            return translation


    def _get_translated_queryset(self):
        """
        Return the queryset that points to the translated model.
        If there is a prefetch, it can be read from this queryset.
        """
        # Get via self.TRANSLATIONS_FIELD.get(..) so it also uses the prefetch/select_related cache.
        accessor = getattr(self, self._translations_field)
        try:
            return accessor.get_queryset()
        except AttributeError:
            # Fallback for Django 1.4 and Django 1.5
            return accessor.get_query_set()


    def save(self, *args, **kwargs):
        super(TranslatableModel, self).save(*args, **kwargs)
        self.save_translations(*args, **kwargs)


    def delete(self, using=None):
        _delete_cached_translations(self)
        super(TranslatableModel, self).delete(using)


    def save_translations(self, *args, **kwargs):
        # Copy cache, new objects (e.g. fallbacks) might be fetched if users override save_translation()
        translations = self._translations_cache.values()

        # Save all translated objects which were fetched.
        # This also supports switching languages several times, and save everything in the end.
        for translation in translations:
            if translation is None:  # Skip fallback markers
                continue

            self.save_translation(translation, *args, **kwargs)


    def save_translation(self, translation, *args, **kwargs):
        # Translation models without any fields are also supported.
        # This is useful for parent objects that have inlines;
        # the parent object defines how many translations there are.
        if translation.is_modified or (translation.is_empty and not translation.pk):
            if not translation.master_id:  # Might not exist during first construction
                translation._state.db = self._state.db
                translation.master = self
            translation.save(*args, **kwargs)


    def safe_translation_getter(self, field, default=None, language_code=None, any_language=False):
        """
        Fetch a translated property, and return a default value
        when both the translation and fallback language are missing.

        When ``any_language=True`` is used, the function also looks
        into other languages to find a suitable value. This feature can be useful
        for "title" attributes for example, to make sure there is at least something being displayed.
        Also consider using ``field = TranslatedField(any_language=True)`` in the model itself,
        to make this behavior the default for the given field.
        """
        # By default, query via descriptor (TranslatedFieldDescriptor)
        # which also attempts the fallback language if configured to do so.
        tr_model = self

        # Extra feature: query a single field from a other translation.
        if language_code and language_code != self._current_language:
            # Try to fetch a cached value first.
            value = get_cached_translated_field(self, language_code, field)
            if value is not None:
                return value

            try:
                tr_model = self._get_translated_model(language_code)
            except TranslationDoesNotExist:
                pass  # Use 'self'

        try:
            return getattr(tr_model, field)
        except TranslationDoesNotExist:
            pass

        if any_language:
            translation = self._get_any_translated_model()
            if translation is not None:
                return getattr(translation, field, default)

        return default


class TranslatedFieldsModelBase(ModelBase):
    """
    Meta-class for the translated fields model.

    It performs the following steps:
    - It validates the 'master' field, in case it's added manually.
    - It tells the original model to use this model for translations.
    - It adds the proxy attributes to the shared model.
    """
    def __new__(mcs, name, bases, attrs):

        # Workaround compatibility issue with six.with_metaclass() and custom Django model metaclasses:
        if not attrs and name == 'NewBase':
            if django.VERSION < (1,5):
                # Let Django fully ignore the class which is inserted in between.
                # Django 1.5 fixed this, see https://code.djangoproject.com/ticket/19688
                attrs['__module__'] = 'django.utils.six'
                attrs['Meta'] = type(str('Meta'), (), {'abstract': True})
            return super(TranslatedFieldsModelBase, mcs).__new__(mcs, name, bases, attrs)

        new_class = super(TranslatedFieldsModelBase, mcs).__new__(mcs, name, bases, attrs)
        if bases[0] == models.Model:
            return new_class

        # No action in abstract models.
        if new_class._meta.abstract or new_class._meta.proxy:
            return new_class

        # Validate a manually configured class.
        shared_model = _validate_master(new_class)

        # Add wrappers for all translated fields to the shared models.
        new_class.contribute_translations(shared_model)

        return new_class


def _validate_master(new_class):
    """
    Check whether the 'master' field on a TranslatedFieldsModel is correctly configured.
    """
    if not new_class.master or not isinstance(new_class.master, ReverseSingleRelatedObjectDescriptor):
        msg = "{0}.master should be a ForeignKey to the shared table.".format(new_class.__name__)
        logger.error(msg)
        raise TypeError(msg)

    shared_model = new_class.master.field.rel.to
    if not issubclass(shared_model, models.Model):
        # Not supporting models.ForeignKey("tablename") yet. Can't use get_model() as the models are still being constructed.
        msg = "{0}.master should point to a model class, can't use named field here.".format(new_class.__name__)
        logger.error(msg)
        raise TypeError(msg)

    if shared_model._translations_model:
        msg = "The model '{0}' already has an associated translation table!".format(shared_model.__name__)
        logger.error(msg)
        raise TypeError(msg)

    return shared_model


class TranslatedFieldsModel(six.with_metaclass(TranslatedFieldsModelBase, models.Model)):
    """
    Base class for the model that holds the translated fields.
    """

    language_code = models.CharField(_("Language"), choices=settings.LANGUAGES, max_length=15, db_index=True)
    master = None   # FK to shared model.

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        signals.pre_translation_init.send(sender=self.__class__, args=args, kwargs=kwargs)
        super(TranslatedFieldsModel, self).__init__(*args, **kwargs)
        self._original_values = self._get_field_values()

        signals.post_translation_init.send(sender=self.__class__, args=args, kwargs=kwargs)

    @property
    def is_modified(self):
        return self._original_values != self._get_field_values()

    @property
    def is_empty(self):
        return len(self.get_translated_fields()) == 0

    @property
    def shared_model(self):
        return self.__class__.master.field.rel.to

    def save_base(self, raw=False, using=None, **kwargs):
        # Send the pre_save signal
        using = using or router.db_for_write(self.__class__, instance=self)
        record_exists = self.pk is not None  # Ignoring force_insert/force_update for now.
        if not self._meta.auto_created:
            signals.pre_translation_save.send(
                sender=self.shared_model, instance=self,
                raw=raw, using=using
            )

        # Perform save
        super(TranslatedFieldsModel, self).save_base(raw=raw, using=using, **kwargs)
        self._original_values = self._get_field_values()
        _cache_translation(self)

        # Send the post_save signal
        if not self._meta.auto_created:
            signals.post_translation_save.send(
                sender=self.shared_model, instance=self, created=(not record_exists),
                raw=raw, using=using
            )

    def delete(self, using=None):
        # Send pre-delete signal
        using = using or router.db_for_write(self.__class__, instance=self)
        if not self._meta.auto_created:
            signals.pre_translation_delete.send(sender=self.shared_model, instance=self, using=using)

        super(TranslatedFieldsModel, self).delete(using=using)
        _delete_cached_translation(self)

        # Send post-delete signal
        if not self._meta.auto_created:
            signals.post_translation_delete.send(sender=self.shared_model, instance=self, using=using)

    def _get_field_values(self):
        # Return all field values in a consistent (sorted) manner.
        return [getattr(self, field.get_attname()) for field, _ in self._meta.get_fields_with_model()]

    @classmethod
    def get_translated_fields(cls):
        # Not using get `get_all_field_names()` because that also invokes a model scan.
        return [f.name for f, _ in cls._meta.get_fields_with_model() if f.name not in ('language_code', 'master', 'id')]

    @classmethod
    def contribute_translations(cls, shared_model):
        """
        Add the proxy attributes to the shared model.
        """
        # Link the translated fields model to the shared model.
        shared_model._translations_model = cls
        shared_model._translations_field = cls.master.field.rel.related_name

        # Assign the proxy fields
        for name in cls.get_translated_fields():
            try:
                # Check if the field already exists.
                # Note that the descriptor even proxies this request, so it should return our field.
                shared_field = getattr(shared_model, name)
            except AttributeError:
                # Add the proxy field for the shared field.
                TranslatedField().contribute_to_class(shared_model, name)
            else:
                # Currently not allowing to replace existing model fields with translatable fields.
                # That would be a nice feature addition however.
                if not isinstance(shared_field, (models.Field, TranslatedFieldDescriptor)):
                    raise TypeError("The model '{0}' already has a field named '{1}'".format(shared_model.__name__, name))

                # When the descriptor was placed on an abstract model,
                # it doesn't point to the real model that holds the _translations_model
                # "Upgrade" the descriptor on the class
                if shared_field.field.model is not shared_model:
                    TranslatedField(any_language=shared_field.field.any_language).contribute_to_class(shared_model, name)


        # Make sure the DoesNotExist error can be detected als shared_model.DoesNotExist too,
        # and by inheriting from AttributeError it makes sure (admin) templates can handle the missing attribute.
        cls.DoesNotExist = type(str('DoesNotExist'), (TranslationDoesNotExist, shared_model.DoesNotExist, cls.DoesNotExist,), {})

    def __unicode__(self):
        # use format to avoid weird error in django 1.4
        # TypeError: coercing to Unicode: need string or buffer, __proxy__ found
        return "{0}".format(get_language_title(self.language_code))

    def __repr__(self):
        return "<{0}: #{1}, {2}, master: #{3}>".format(
            self.__class__.__name__, self.pk, self.language_code, self.master_id
        )
