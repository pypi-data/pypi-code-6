from django.conf import settings
from django.conf.urls import url
from django.db.models.base import ModelBase
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView

from oak.views import *


class Hub(object):
    """

    """
    model_registrations = {}
    view_registrations = {}

    def __init__(self):
        """

        """
        apps = [ app for app in settings.INSTALLED_APPS if not "django" in app and not "oak" in app]
        for app in apps:
            try:
                __import__('%s.views' % app, globals(), locals())
            except (ImportError):
                pass

    @classmethod
    def register_view(cls, view, **kwargs):
        allowed = False
        for allowed_type in [CreateView, UpdateView, DeleteView, DetailView, ListView, BaseCrudView]:
            if issubclass(view, allowed_type):
                allowed = True
                break

        if not allowed:
            raise Exception("Cannot register object '%s'. Not supported." % view.__class__)

        key = str(view)

        if key in cls.view_registrations:
            return

        d = kwargs.copy()
        d['view'] = view
        cls.view_registrations[key] = d

    @classmethod
    def register_model(cls, model, **kwargs):
        if not isinstance(model, ModelBase):
            raise Exception("Cannot register object '%s'. Not supported." % model.__class__)

        key = "%s.%s" % (model._meta.app_label, model._meta.model_name)

        if key in cls.model_registrations:
            return

        d = kwargs.copy()
        d['model'] = model
        cls.model_registrations[key] = d

    def _get_create_view(self, app_label, model_name, view, options):
        return url(r'%s%s' % (app_label and '%s/' % app_label or '', '%s/create/$' % model_name),
                   view.__class__.as_view(), name='%s-%s-create' % (app_label, model_name))

    def _get_update_view(self, app_label, model_name, view, options):
        return url(r'%s%s' % (app_label and '%s/' % app_label or '', '%s/update/(?P<pk>\d+)/$' % model_name),
                   view.__class__.as_view(), name='%s-%s-update' % (app_label, model_name))

    def _get_delete_view(self, app_label, model_name, view, options):
        return url(r'%s%s' % (app_label and '%s/' % app_label or '', '%s/delete/(?P<pk>\d+)/$' % model_name),
                   view.__class__.as_view(), name='%s-%s-delete' % (app_label, model_name))

    def _get_detail_view(self, app_label, model_name, view, options):
        return url(r'%s%s' % (app_label and '%s/' % app_label or '', '%s/(?P<pk>\d+)/' % model_name),
                   view.__class__.as_view(), name='%s-%s' % (app_label, model_name))

    def _get_list_view(self, app_label, model_name, view, options):
        return url(r'%s%s' % (app_label and '%s/' % app_label or '', '%s/list/$' % model_name),
                   view.__class__.as_view(), name='%s-%s-list' % (app_label, model_name))

    def get_urls(self):
        """

        """
        patterns = []
        for v in self.view_registrations.values():
            view = v.get('view')
            app_label = v.get('app_label', view.model._meta.app_label)
            model_name = v.get('model_name', view.model._meta.model_name)

            if issubclass(view, BaseCrudView):
                model = view.model

                create_view = type('%s%sCreateView' % (app_label, model_name), (view, BaseCreateView,),
                                   {'model': model, 'oak_enabled': True, 'fields': view.fields})

                update_view = type('%s%sUpdateView' % (app_label, model_name), (view, BaseUpdateView,),
                                   {'model': model, 'oak_enabled': True, 'fields': view.fields})

                delete_view = type('%s%sDeleteView' % (app_label, model_name), (view, BaseDeleteView,),
                                   {'model': model, 'oak_enabled': True})

                patterns.append(self._get_create_view(app_label, model_name, create_view(), v))
                patterns.append(self._get_update_view(app_label, model_name, update_view(), v))
                patterns.append(self._get_delete_view(app_label, model_name, delete_view(), v))
                continue

            setattr(view, 'oak_enabled', True)
            if issubclass(view, CreateView):
                patterns.append(self._get_create_view(app_label, model_name, view(), v))

            elif issubclass(view, UpdateView):
                patterns.append(self._get_update_view(app_label, model_name, view(), v))

            elif issubclass(view, DeleteView):
                patterns.append(self._get_delete_view(app_label, model_name, view(), v))

            elif issubclass(view, DetailView):
                patterns.append(self._get_detail_view(app_label, model_name, view(), v))

            elif issubclass(view, ListView):
                patterns.append(self._get_list_view(app_label, model_name, view(), v))

        for m in self.model_registrations.values():
            model = m.get('model')
            app_label = m.get('app_label', model._meta.app_label)
            model_name = m.get('model_name', model._meta.model_name)

            detail_view = type('%s%sDetailView' % (app_label, model_name), (BaseDetailView,), {'model': model, 'oak_enabled': True})
            create_view = type('%s%sCreateView' % (app_label, model_name), (BaseCreateView,), {'model': model, 'oak_enabled': True})
            update_view = type('%s%sUpdateView' % (app_label, model_name), (BaseUpdateView,), {'model': model, 'oak_enabled': True})
            delete_view = type('%s%sDeleteView' % (app_label, model_name), (BaseDeleteView,), {'model': model, 'oak_enabled': True})
            list_view = type('%s%sListView' % (app_label, model_name), (BaseListView,), {'model': model, 'oak_enabled': True, 'pagination_by': 25})
            patterns.append(self._get_detail_view(app_label, model_name, detail_view(), m))
            patterns.append(self._get_create_view(app_label, model_name, create_view(), m))
            patterns.append(self._get_update_view(app_label, model_name, update_view(), m))
            patterns.append(self._get_delete_view(app_label, model_name, delete_view(), m))
            patterns.append(self._get_list_view(app_label, model_name, list_view(), m))

        return tuple(patterns)

# TODO:
#  if issubclass(view, ArchiveIndexView):
#         # ArchiveIndexView.as_view(model=Article, date_field="pub_date")
#         return [url(r'%(app_label)s/%(object_name)s/archive/$' % data, view.as_view(),
#                     name="%(app_label)s-%(object_name)s-archive" % data)]
#
#     if issubclass(view, YearArchiveView):
#         return [url(r'%(app_label)s/%(object_name)s/(?P<year>\d{4})/$' % data, view.as_view(),
#                     name="%(app_label)s-%(object_name)s-year-archive" % data)]
#
#     if issubclass(view, MonthArchiveView):
#    # Example: /2012/aug/
# #     url(r'^(?P<year>\d{4})/(?P<month>[-\w]+)/$',
# #         ArticleMonthArchiveView.as_view(month_format='%m'),
#         return [url(r'%(app_label)s/%(object_name)s/(?P<year>\d{4})/(?P<month>\d+)/$' % data, view.as_view(),
#                     name="%(app_label)s-%(object_name)s-archive-month" % data)]
#
#     if issubclass(view, WeekArchiveView):
#         raise Exception("Not implemented yet")
#
#     if issubclass(view, DayArchiveView):
#         return [url(r'%(app_label)s/%(object_name)s/(?P<year>\d{4})/(?P<month>[-\w]+)/(?P<day>\d+)/$' % data,
#                     view.as_view(), name="%(app_label)s-%(object_name)s-archive-day" % data)]
#
#     if issubclass(view, TodayArchiveView):
#         return [url(r'%(app_label)s/%(object_name)s/today/$' % data, view.as_view(),
#                     name="%(app_label)s-%(object_name)s-archive-today" % data)]
#
#     if issubclass(view, DateDetailView):
#         #DateDetailView.as_view(model=Article, date_field="pub_date"),
#         return [url(r'%(app_label)s/%(object_name)s/(?P<year>\d+)/(?P<month>[-\w]+)/(?P<day>\d+)/(?P<pk>\d+)/$' %
#                     data, view.as_view(),
#                     name="%(app_label)s-%(object_name)s-archive-date-detail" % data)]