# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webapp.views',
    url(r'^$', 'home', name='home'),

    # STUDENT
    url(r'student/view/$', 'student_view', name='student_view'),
    url(r'student/(?P<pk>\d+)/view/$', 'student_view', name='student_view'),
    url(r'student/(?P<pk>\d+)/delete/$', 'student_delete', name='student_delete'),
    url(r'student/(?P<pk>\d+)/edit/$', 'student_edit', name='student_edit'),
    url(r'student/add/$', 'student_add', name='student_add'),
    # url(r'student/(?P<pk>\d+)/career/(?P<pk>\d+)/$', 'career_assign', name='career_assign'),

    # TEACHER
    url(r'teacher/view/$', 'teacher_view', name='teacher_view'),
    url(r'teacher/(?P<pk>\d+)/view/$', 'teacher_view', name='teacher_view'),
    url(r'teacher/(?P<pk>\d+)/delete/$', 'teacher_delete', name='teacher_delete'),
    url(r'teacher/(?P<pk>\d+)/edit/$', 'teacher_edit', name='teacher_edit'),
    url(r'teacher/add/$', 'teacher_add', name='teacher_add'),

    # QUIZ
    url(r'quiz/view/$', 'quiz_view', name='quiz_view'),
    url(r'quiz/(?P<pk>\d+)/view/$', 'quiz_view', name='quiz_view'),
    url(r'quiz/(?P<pk>\d+)/delete/$', 'quiz_delete', name='quiz_delete'),
    url(r'quiz/(?P<pk>\d+)/edit/$', 'quiz_edit', name='quiz_edit'),
    url(r'quiz/add/$', 'quiz_add', name='quiz_add'),
    url(r'quiz/(?P<pk>\d+)/question/add/$', 'quiz_add_question', name='quiz_add_question'),

    # CAREER
    url(r'career/view/$', 'career_view', name='career_view'),
    url(r'career/(?P<pk>\d+)/view/$', 'career_view', name='career_view'),
    url(r'career/(?P<pk>\d+)/delete/$', 'career_delete', name='career_delete'),
    url(r'career/(?P<pk>\d+)/edit/$', 'career_edit', name='career_edit'),
    url(r'career/add/$', 'career_add', name='career_add'),
)

