from django.contrib import admin
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.http import urlquote
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from feincms.admin import item_editor
from feincms import ensure_completely_loaded

from djapps.blogs.models import Blog, Post


class BlogAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'posts',
        'new_post',
    ]
    search_fields = [
        'name',
        'slug'
    ]
    prepopulated_fields = {'slug': ('name',)}

    def posts(self, obj):
        """Provides a link to the blog specific post admin changelist page"""
        return mark_safe(
            '<a href="%s?blog__id__exact=%d">%d posts...</a>' % (
                escape(reverse("admin:blogs_post_changelist")),
                obj.id,
                obj.posts.count(),
            )
        )

    def new_post(self, obj):
        """Provides a link to the blog specific post admin add page"""
        return mark_safe(
            '<a href="%s?_changelist_filters=%s">New post...</a>' % (
                escape(reverse("admin:blogs_post_add")),
                urlquote("blog__id__exact=%d" % obj.id),
            )
        )


class PostAdmin(item_editor.ItemEditor):
    date_hierarchy = 'date'
    list_display = [
        'title',
        'blog',
        'date',
        'time',
        'published',
    ]
    list_filter = [
        'blog',
        'published',
        'date',
    ]
    search_fields = [
        'title',
        'slug',
    ]
    prepopulated_fields = {'slug': ('title',)}
    radio_fields = {'template_key': admin.HORIZONTAL}

    fieldset_insertion_index = 2
    fieldsets = [
        (None, {
            'fields': [
                'blog',
                ('title', 'slug'),
                ('published'),
            ],
        }),
        ('Other options', {
            'classes': ['collapse'],
            'fields': ['template_key', ['date', 'time']],
        }),
        # <-- insertion point, extensions appear here, see insertion_index
        # above
        item_editor.FEINCMS_CONTENT_FIELDSET,
    ]

    def __init__(self, model, admin_site):
        ensure_completely_loaded()

        if len(model._feincms_templates) > 4 and \
                'template_key' in self.radio_fields:
            del(self.radio_fields['template_key'])

        super(PostAdmin, self).__init__(model, admin_site)

    def add_view(self, request, *args, **kwargs):
        """Add initial blog value if needed"""
        old_GET = request.GET
        GET = request.GET.copy()
        if 'blog' not in request.GET.keys():
            filters = GET.get('_changelist_filters', '')
            filters = filters.split('&')
            filters = [f.split('=', 1) for f in filters]
            filters = [f for f in filters if len(f) == 2]
            filters = dict(filters)
            blog_id = filters.get('blog__id__exact', None)
            if blog_id is None:
                try:
                    blog_id = Blog.objects.get().id
                except (ObjectDoesNotExist, MultipleObjectsReturned):
                    pass

            if blog_id is not None:
                GET['blog'] = blog_id

        try:
            request.GET = GET
            return super(PostAdmin, self).add_view(request, *args, **kwargs)
        finally:
            request.GET = old_GET


if getattr(settings, "FEINCMS_BLOGS_USE_BLOG_ADMIN", True):
    admin.site.register(Blog, BlogAdmin)

if getattr(settings, "FEINCMS_BLOGS_USE_POST_ADMIN", True):
    admin.site.register(Post, PostAdmin)
