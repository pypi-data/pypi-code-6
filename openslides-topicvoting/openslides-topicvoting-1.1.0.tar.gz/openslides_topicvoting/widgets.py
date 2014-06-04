# -*- coding: utf-8 -*-
"""
Dashboard widget for the plugin.
"""

from django.utils.translation import ugettext_lazy

from openslides.projector.api import get_active_slide
from openslides.utils.widgets import Widget

from .models import Category


class TopicvotingWidget(Widget):
    """
    Provides a widget to control the topicvoting slides.
    """
    name = 'topicvoting'
    verbose_name = ugettext_lazy('Topicvoting')
    required_permission = 'core.can_manage_projector'
    default_weight = 210
    template_name = 'openslides_topicvoting/widget_category.html'
    icon_css_class = 'icon-podium'
    more_link_pattern_name = 'topicvoting_category_list'

    def get_context_data(self, **context):
        return super(TopicvotingWidget, self).get_context_data(
            category_list=Category.objects.all(),
            category_list_slide_is_active=get_active_slide()['callback'] == 'topicvoting_category_list',
            result_slide_is_active=get_active_slide()['callback'] == 'topicvoting_result',
            **context)
