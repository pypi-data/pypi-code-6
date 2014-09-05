# -- coding:utf-8 --
import datetime

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from huron.blog.models import Post


class LatestEntriesFeed(Feed):
    title = _("Rss Feed")
    link = reverse('blog:blog_general')
    description = _("Last entries from blog.")

    def items(self):
        return Post.objects.get_published().order_by('-pub_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.article
