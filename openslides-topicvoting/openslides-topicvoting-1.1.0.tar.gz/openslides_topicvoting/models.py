# -*- coding: utf-8 -*-
"""
Model classes for categories and topics.
"""

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.translation import pgettext_lazy, ugettext_lazy, ugettext_noop

from openslides.projector.api import get_active_slide, update_projector
from openslides.projector.models import SlideMixin


class Category(SlideMixin, models.Model):
    """
    The model for categories of topics.
    """
    slide_callback_name = 'topicvoting_category'
    """
    The callback_name for the slides.
    """

    name = models.CharField(max_length=255, verbose_name=ugettext_lazy('Name'))
    """
    A string, the name of the category of topics.
    """

    weight = models.IntegerField(default=0, verbose_name=ugettext_lazy('Weight (for runoff poll)'))
    """
    An integer. A higher value prioritises the category in result view
    and slide. This can be used if there was a runoff poll.
    """

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        """
        Method for representation.
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Updates the projector if a topicvoting slide is on it.
        """
        value = super(Category, self).save(*args, **kwargs)
        callback = get_active_slide()['callback']
        if callback == 'topicvoting_category_list' or callback == 'topicvoting_result':
            update_projector()
        return value

    def get_absolute_url(self, link='update'):
        """
        Gets the url of the update view or the delete view of a category instance.
        """
        if link == 'update':
            url = reverse('topicvoting_category_update', args=[str(self.id)])
        elif link == 'delete':
            url = reverse('topicvoting_category_delete', args=[str(self.id)])
        else:
            url = super(Category, self).get_absolute_url(link)
        return url

    @property
    def sum_of_votes(self):
        """
        Returns the sum of all votes of the topic of a category as integer.
        """
        sum_of_votes = 0
        for topic in self.topic_set.all():
            if topic.votes:
                sum_of_votes += topic.votes
        return sum_of_votes

    def get_votes_string(self):
        """
        Returns the sum of votes and, as ths case may be, the weight as string.
        """
        if self.weight:
            string = '%d / %d' % (self.sum_of_votes, self.weight)
        else:
            string = str(self.sum_of_votes)
        return string


class Topic(models.Model):
    """
    The model for topics.
    """

    title = models.CharField(max_length=255, verbose_name=ugettext_lazy('Title'))
    """
    A string, the name of the topic.
    """

    submitter = models.CharField(max_length=255, blank=True, verbose_name=ugettext_lazy('Submitter'))  # TODO: Change this to a person field
    """
    A string, the name of the submitter of the topic.
    """

    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, verbose_name=pgettext_lazy('topicvoting', 'Category'))
    """
    A foreign key to a category the topic belongs to. If it is None, the
    topic is a ‘lost topic’. Deleting a category will become their topics
    lost.
    """

    votes = models.IntegerField(null=True, blank=True, verbose_name=ugettext_lazy('Votes'))
    """
    An integer, the votes for this topic. The OpenSlides poll system is
    not available yet.
    """

    weight = models.IntegerField(default=0, verbose_name=ugettext_lazy('Weight (for runoff poll)'))
    """
    An integer. A higher value prioritises the topic in result view
    and slide. This can be used if there was a runoff poll.
    """

    class Meta:
        ordering = ('title',)
        permissions = (
            ('can_see', ugettext_noop('Can see topicvoting categories and topics')),
            ('can_manage', ugettext_noop('Can manage topicvoting categories and topics')),)

    def __unicode__(self):
        """
        Method for representation.
        """
        if self.submitter:
            return _('%(title)s (proposed by %(submitter)s)') % {'title': self.title, 'submitter': self.submitter}
        else:
            return self.title

    def save(self, *args, **kwargs):
        """
        Updates the projector if a topicvoting slide is on it.
        """
        # TODO: Look for all cases and switch off unused update
        value = super(Topic, self).save(*args, **kwargs)
        callback = get_active_slide()['callback']
        if callback and callback.startswith('topicvoting'):
            update_projector()
        return value

    def get_absolute_url(self, link='update'):
        """
        Gets the url of the update view or the delete view of a topic instance.
        """
        if link == 'update':
            url = reverse('topicvoting_topic_update', args=[str(self.id)])
        elif link == 'delete':
            url = reverse('topicvoting_topic_delete', args=[str(self.id)])
        else:
            url = super(Topic, self).get_absolute_url(link)
        return url

    def get_votes_string(self):
        """
        Returns the votes and, as ths case may be, the weight as string.
        """
        if self.weight:
            string = '%d / %d' % (self.votes, self.weight)
        else:
            string = str(self.votes)
        return string

    def get_title_with_votes(self):
        """
        Gets the title and the votes if there are some.
        """
        if self.votes is not None:
            title = '%s (%s)' % (self.title, self.get_votes_string())
        else:
            title = self.title
        return title
