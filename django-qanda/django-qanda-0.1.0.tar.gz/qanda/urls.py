from django.conf.urls import url
from .views import TopicDetail, TopicList, QuestionDetail


urlpatterns = [

    url(r'^$',
        TopicList.as_view(),
        name='qanda.views.topiclist'
        ),
    url(r'^(?P<topic_slug>[\w-]+)/$',
        TopicDetail.as_view(),
        name='qanda.views.topicdetail'
        ),
    url(r'^(?P<topic_slug>[\w-]+)/(?P<question_slug>[\w-]+)/$',
        QuestionDetail.as_view(),
        name='qanda.views.questiondetail'
        ),
    ]
