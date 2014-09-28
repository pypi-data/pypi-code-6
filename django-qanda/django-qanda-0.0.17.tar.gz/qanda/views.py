# Django
from django.conf import settings
from django.http import Http404
from django.views.generic import ListView, DetailView

# Local
from .models import Question, Topic
from .mixins import QuestionQuerysetMixin, TopicQuestionsMixin

RECENT_UPDATES_COUNT = getattr(settings, 'QANDA_RECENT_UPDATES_COUNT', 7)


class TopicList(QuestionQuerysetMixin, ListView):
    model = Topic
    template_name = 'qanda/topic_list.html'
    allow_empty = True
    questions_context_object_name = 'related_questions'

    def get_queryset(self):
        # Check for access level
        if self.request.user.is_staff:
            return self.model.objects.for_staff()

        if self.request.user.is_authenticated():
            return self.model.objects.for_members()

        return self.model.objects.for_anonymous()

    def get_context_data(self, **kwargs):
        context = super(TopicList, self).get_context_data(**kwargs)
        context_name = self.questions_context_object_name
        questions = self.get_question_queryset()
        if questions:
            questions = questions.order_by('-modified')
            context[context_name] = questions[:RECENT_UPDATES_COUNT]
        return context


class TopicDetail(TopicQuestionsMixin, DetailView):
    template_name = 'qanda/topic_detail.html'
    slug_url_kwarg = 'topic_slug'

    def get_object(self):
        if not self.queryset:
            raise Http404('No questions for that topic')
        return self.topic


class QuestionDetail(TopicQuestionsMixin, DetailView):
    template_name = 'qanda/question_detail.html'
    slug_url_kwarg = 'question_slug'

    def get_object(self):
        qs = self.queryset.filter(topic=self.topic)
        return super(QuestionDetail, self).get_object(qs)
