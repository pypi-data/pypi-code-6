from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from feincms_template_content.models import TemplateContent

from djapps.blogs.models import Blog, Post
from djapps.blogs.views import PostView


@python_2_unicode_compatible
class RecentPostsListContent(TemplateContent):
    class Meta(object):
        abstract = True
        verbose_name = 'recent posts list'
        verbose_name_plural = 'recent posts lists'

    blog = models.ForeignKey(Blog, verbose_name=_('blog'),
                             blank=True, null=True)
    max_posts = models.PositiveIntegerField(_('posts'), default=5)
    offeset = models.PositiveIntegerField(_('offeset'), default=0)

    def __str__(self):
        return u"%d blog posts from %s" % (
            self.max_posts or 0,
            self.blog if self.blog_id else "all blogs",
        )

    def posts(self):
        if self.blog:
            posts = self.blog.posts.active()
        else:
            posts = Post.objects.active()
        return posts[self.offeset:self.offeset+self.max_posts]

class BlogArchiveContent(TemplateContent):
    class Meta(object):
        abstract = True
        verbose_name = 'blog archive'
        verbose_name_plural = 'blog archives'

    blog = models.ForeignKey(Blog, verbose_name=_('blog'),
                             blank=True, null=True)

    def __str__(self):
        return u"%s archive %s" % (
            self.blog if self.blog_id else None,
        )
