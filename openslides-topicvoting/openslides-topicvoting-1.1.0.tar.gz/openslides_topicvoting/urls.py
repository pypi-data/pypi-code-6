# -*- coding: utf-8 -*-
"""
Url patterns.
"""

from django.conf.urls import include, patterns, url

from . import views

extra_patterns = patterns(
    '',

    # Categories and Topics
    url(r'^$',
        views.TopicvotingCategoryListView.as_view(),
        name='topicvoting_category_list'),

    # Category
    url(r'^category/create/$',
        views.TopicvotingCategoryCreateView.as_view(),
        name='topicvoting_category_create'),
    url(r'^category/(?P<pk>\d+)/update/$',
        views.TopicvotingCategoryUpdateView.as_view(),
        name='topicvoting_category_update'),
    url(r'^category/(?P<pk>\d+)/delete/$',
        views.TopicvotingCategoryDeleteView.as_view(),
        name='topicvoting_category_delete'),

    # Topic
    url(r'^topic/create/$',
        views.TopicvotingTopicCreateView.as_view(),
        name='topicvoting_topic_create'),
    url(r'^topic/(?P<pk>\d+)/update/$',
        views.TopicvotingTopicUpdateView.as_view(),
        name='topicvoting_topic_update'),
    url(r'^topic/(?P<pk>\d+)/delete/$',
        views.TopicvotingTopicDeleteView.as_view(),
        name='topicvoting_topic_delete'),

    # Import
    url(r'^import/csv/$',
        views.TopicvotingCSVImportView.as_view(),
        name='topicvoting_import_csv'),

    # Ballot paper
    url(r'^ballotpaper/$',
        views.TopicvotingCategoryListView.as_view(template_name='openslides_topicvoting/ballotpaper.html'),
        name='topicvoting_ballotpaper'),

    # Voting result
    url(r'^result/$',
        views.TopicvotingResultView.as_view(),
        name='topicvoting_result'),
    url(r'^result/print/$',
        views.TopicvotingResultView.as_view(template_name='openslides_topicvoting/result_print.html'),
        name='topicvoting_result_print'))


urlpatterns = patterns(
    '',
    url(r'^topicvoting/', include(extra_patterns)))
