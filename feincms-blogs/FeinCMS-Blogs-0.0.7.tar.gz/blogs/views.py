import datetime

from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView
from django.views.generic.base import View
from django.utils.translation import ugettext as _
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

from feincms.module.mixins import ContentView

from djapps.blogs.models import Blog, Post


class PostPermalinkView(SingleObjectMixin, View):
    model = Post

    def get_queryset(self):
        return self.model.objects.active()

    def get(self, request, *args, **kwargs):
        post = self.get_object()

        return HttpResponseRedirect(
            post.get_pretty_url()
        )


class PostView(ContentView):
    model = Post
    context_object_name = 'post'

    def get_queryset(self):
        return self.model.objects.active().filter(**self.kwargs)

    def get_context_data(self, *args, **kwargs):
        data = super(PostView, self).get_context_data(*args, **kwargs)
        self.request._blogs_current_blog = self.object.blog
        self.request._blogs_current_date = self.object.date
        self.request._blogs_current_year = int(self.kwargs.get('date__year', 0))
        self.request._blogs_current_month = int(self.kwargs.get('date__month', 0))
        self.request._blogs_current_day = int(self.kwargs.get('date__day', 0))
        return data

    def get_object(self):
        queryset = self.get_queryset()

        obj = queryset.first()
        if obj is None:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class PostListView(ListView):
    model = Post
    paginate_by = 15

    def dispatch(self, *args, **kwargs):
        try:
            self.range_start = datetime.date(
                year=int(self.kwargs.get("date__year", 1)),
                month=int(self.kwargs.get("date__month", 1)),
                day=int(self.kwargs.get("date__day", 1)),
            )
        except ValueError:
            raise Http404(_("Invalid date"))

        return super(PostListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.model.objects.active().filter(
            **dict(
                (k, v) for k,v in self.kwargs.items()
            )
        )

    def get_context_data(self, *args, **kwargs):
        data = super(PostListView, self).get_context_data(*args, **kwargs)
        data["range_start"] = self.range_start
        data["year"] = self.kwargs.get('date__year', None)
        data["month"] = self.kwargs.get('date__month', None)
        data["day"] = self.kwargs.get('date__day', None)
        blogslug = self.kwargs.get('blog__slug', False)
        if blogslug:
            blog = Blog.objects.filter(slug=blogslug).first()
            if blog is None:
                raise Http404(_("Blog not found"))
            data["blog"] = blog
            self.request._blogs_current_blog = blog
        self.request._blogs_current_date = self.range_start
        self.request._blogs_current_year = int(self.kwargs.get('date__year', 0))
        self.request._blogs_current_month = int(self.kwargs.get('date__month', 0))
        self.request._blogs_current_day = int(self.kwargs.get('date__day', 0))
        return data
