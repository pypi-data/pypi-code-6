"""
Django Feedme

Views.py

Author: Derek Stegelman
"""
import logging

from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, FormView, CreateView
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from infuse.auth.permissions import LoginRequiredMixin

from .models import Feed, FeedItem, Category
from .forms import AddFeedForm, ImportFeedForm
from .google_takeout import GoogleReaderTakeout
from .mixins import AjaxableResponseMixin

logger = logging.getLogger(__name__)


class FeedList(LoginRequiredMixin, ListView):
    """
    Show the feed list for the logged in user.
    """
    template_name = 'feedme/feed_list.html'
    context_object_name = 'feed_items'

    def _update_feeds(self, user):
        """
        Update the feeds.  We try to do this
        on page load in case we don't have the
        most updated feeds.
        """
        for feed in Feed.objects.filter(user=user):
            feed.update()
        return True

    def get_queryset(self):
        """
        Overwrite the query set method.  Updates the feeds
        and then checks to see if the user is passing a feed id
        or category.
        """
        # Update the feed on page load..
        self._update_feeds(self.request.user)
        items = FeedItem.objects.my_feed_items(self.request.user).un_read()

        if self.kwargs.get('category', None):
            return items.category(self.kwargs.get('category'))

        if self.kwargs.get('feed_id', None):
            return items.filter(feed__id=self.kwargs.get('feed_id'))

        return items

    def get_context_data(self, **kwargs):
        """
        Update the context data.  Add the categories and
        push the FeedForm to the template.
        """
        context = super(FeedList, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(user=self.request.user)
        context['add_form'] = AddFeedForm()

        return context


class ImportView(LoginRequiredMixin, FormView):
    """
    Main view for importing feeds from Google Reader.
    """
    template_name = 'feedme/takeout_form.html'
    form_class = ImportFeedForm
    success_url = 'feedme-feed-list'

    def get_context_data(self, **kwargs):
        """
        Push extra context to the template.
        :param kwargs:
        :return:
        """
        context = super(ImportView, self).get_context_data(**kwargs)
        context['add_form'] = AddFeedForm()
        context['form'] = ImportFeedForm(user=self.request.user)

        return context

    def form_valid(self, form):
        """
        Process the form.
        """
        takeout = GoogleReaderTakeout(self.request.FILES['archive'])
        for data in takeout.subscriptions():
            if not data['xmlUrl']:
                logger.info("Found feed without url. Dumping %s." % data['title'])
                continue
            if data['category']:
                category, created = Category.objects.get_or_create(name=data['category'], user=self.request.user)
            else:
                category = form.cleaned_data['category']
            Feed.objects.get_or_create(
                url=data['xmlUrl'], title=data['title'],
                user=self.request.user, last_update=None,
                category=category
            )

        return redirect(reverse(self.get_success_url()))


class AddView(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    """
    Simple class based create view
    """
    form_class = AddFeedForm
    model = Feed


def mark_all_as_read(request):
    """
    Marks all items for a user as read.
    """
    items = FeedItem.objects.my_feed_items(request.user).un_read()

    for item in items:
        item.mark_as_read()

    return redirect('feedme-feed-list')


@csrf_exempt
def mark_as_read(request):
    """
    Ajax method to mark an item as being read.
    :param request:
    :return AJAX/HTTP Response of 200:
    """
    if request.method == "POST":
        feed_item = get_object_or_404(FeedItem, pk=request.POST.get('feed_item_id'))
        feed_item.read = True
        feed_item.save()

    return HttpResponse()
