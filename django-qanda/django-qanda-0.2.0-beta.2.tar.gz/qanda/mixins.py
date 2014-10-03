"""
Mixins for qanda.views
"""

# Django
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

# Local
from .models import Question, Topic


class QuestionQuerysetMixin(object):
    question_queryset = Question.published

    def get_question_queryset(self):
        queryset = self.question_queryset

        # Check for access level
        if self.request.user.is_staff:
            pass
        elif self.request.user.is_authenticated():
            queryset = queryset.for_members()
        else:
            queryset = queryset.for_anonymous()
        return queryset


class TopicQuestionsMixin(QuestionQuerysetMixin):
    topic_queryset = Topic.objects
    context_object_list_name = None

    @cached_property
    def queryset(self):
        """
        Override the queryset property filtering by both questions and topic.
        """
        return self.get_question_queryset().filter(topic=self.topic)

    @cached_property
    def topic(self):
        return get_object_or_404(
            self.topic_queryset,
            slug__exact=self.kwargs['topic_slug']
            )

    def get_context_object_list_name(self, object_list):
        """
        Get the name of the object_list to be used in the context.
        """
        if self.context_object_list_name:
            return self.context_object_list_name
        elif hasattr(object_list, 'model'):
            return '%s_list' % object_list.model._meta.model_name
        else:
            return None

    def get_context_data(self, **kwargs):
        """
        Insert the context_object_list into the template context.
        """
        context = super(TopicQuestionsMixin, self).get_context_data(**kwargs)
        list_name = self.get_context_object_list_name(self.queryset)
        if list_name is not None:
            context[list_name] = self.queryset
        return context
