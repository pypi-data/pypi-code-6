# -*- coding: utf-8 -*-
"""
Slides for the category model, an overview of all categories and for the results.
"""

from django.template.loader import render_to_string
from openslides.config.api import config
from openslides.projector.api import register_slide, register_slide_model

from .models import Category
from .voting_system import Hoechstzahl, feed_hoechstzahls


def category_slide_list(**kwargs):
    """
    Slide to show an overview of all categories.
    """
    context = {'category_list': Category.objects.all()}
    return render_to_string('openslides_topicvoting/category_slide_list.html', context)


def result_slide(**kwargs):
    """
    Slide to show a table with all voting results. The winning topics are given too.
    """
    feed_hoechstzahls()
    result_table_and_info = Hoechstzahl.get_result_table_and_info()
    context = {'result_table': result_table_and_info['result_table'],
               'winning_topics': result_table_and_info['winning_topics'],
               'runoff_poll_warning': result_table_and_info['runoff_poll_warning'],
               'topic_post_warning': result_table_and_info['topic_post_warning'],
               'divisors': map(lambda rank: rank * 2 + 1, range(max(config['openslides_topicvoting_posts'], 3)))}
    return render_to_string('openslides_topicvoting/result_slide.html', context)


register_slide_model(Category, 'openslides_topicvoting/category_slide.html')
register_slide('topicvoting_category_list', category_slide_list)
register_slide('topicvoting_result', result_slide)
