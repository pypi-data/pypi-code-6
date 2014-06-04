# -*- coding: utf-8 -*-
"""
Views for categories and topics.
"""

from openslides.config.api import config
from openslides.utils.views import CSVImportView, ListView, CreateView, UpdateView, DeleteView

from .csv_import import import_categories_and_topics
from .models import Category, Topic
from .voting_system import Hoechstzahl, feed_hoechstzahls


class TopicvotingCategoryListView(ListView):
    """
    View to list all categories and all topics.
    """
    model = Category
    required_permission = 'openslides_topicvoting.can_see'

    def get_context_data(self, **kwargs):
        context = super(TopicvotingCategoryListView, self).get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        context['lost_topics'] = Topic.objects.filter(category=None).exists()
        return context


class TopicvotingCategoryCreateView(CreateView):
    model = Category
    success_url_name = 'topicvoting_category_list'
    url_name_args = []
    required_permission = 'openslides_topicvoting.can_manage'


class TopicvotingCategoryUpdateView(UpdateView):
    model = Category
    success_url_name = 'topicvoting_category_list'
    url_name_args = []
    required_permission = 'openslides_topicvoting.can_manage'


class TopicvotingCategoryDeleteView(DeleteView):
    model = Category
    success_url_name = 'topicvoting_category_list'
    url_name_args = []
    required_permission = 'openslides_topicvoting.can_manage'


class TopicvotingTopicCreateView(CreateView):
    model = Topic
    success_url_name = 'topicvoting_category_list'
    url_name_args = []
    required_permission = 'openslides_topicvoting.can_manage'


class TopicvotingTopicUpdateView(UpdateView):
    model = Topic
    success_url_name = 'topicvoting_category_list'
    url_name_args = []
    required_permission = 'openslides_topicvoting.can_manage'


class TopicvotingTopicDeleteView(DeleteView):
    model = Topic
    success_url_name = 'topicvoting_category_list'
    url_name_args = []
    required_permission = 'openslides_topicvoting.can_manage'


class TopicvotingCSVImportView(CSVImportView):
    """
    View to import categories and topics using a csv file.
    """
    import_function = staticmethod(import_categories_and_topics)
    required_permission = 'openslides_topicvoting.can_manage'
    template_name = 'openslides_topicvoting/csv_import.html'
    success_url_name = 'topicvoting_category_list'


class TopicvotingResultView(TopicvotingCategoryListView):
    """
    View to show the results in a nice table.
    """
    template_name = 'openslides_topicvoting/result.html'
    required_permission = 'openslides_topicvoting.can_see'

    def get_context_data(self, **kwargs):
        """
        Inserts the results table and additional flags and variables into the context.
        """
        context = super(TopicvotingResultView, self).get_context_data(**kwargs)
        feed_hoechstzahls()
        result_table_and_info = Hoechstzahl.get_result_table_and_info()
        context['result_table'] = result_table_and_info['result_table']
        context['winning_topics'] = result_table_and_info['winning_topics']
        context['runoff_poll_warning'] = result_table_and_info['runoff_poll_warning']
        context['topic_post_warning'] = result_table_and_info['topic_post_warning']
        context['divisors'] = map(lambda rank: rank * 2 + 1, range(max(config['openslides_topicvoting_posts'], 3)))
        return context
