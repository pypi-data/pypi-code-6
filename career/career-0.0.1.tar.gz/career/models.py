# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from hvad.models import TranslatableModel, TranslatedFields
from hvad.manager import TranslationManager

class Quiz(TranslatableModel):
    short_description = models.CharField(max_length=128)
    translations = TranslatedFields(
        title = models.CharField(max_length=256, null=True, blank=True),
        description = models.TextField(null=True, blank=True)
    )

    def __unicode__(self):
        return u'%s' % self.short_description

    def get_questions(self):
        return Question.objects.get_questions_for_quiz(self.id)

    class Meta:
        verbose_name_plural = 'Quizzes'


class Answer(TranslatableModel):
    short_description = models.CharField(max_length=128)
    translations = TranslatedFields(
        description = models.TextField(null=True, blank=True)
    )


class QuestionManager(TranslationManager):
    def get_questions_for_quiz(self, quiz):
        return self.get_query_set().filter(quiz=quiz).order_by('order')

class Question(TranslatableModel):
    short_description = models.CharField(max_length=128)
    quiz = models.ForeignKey('Quiz')
    order = models.IntegerField(null=True, blank=True)
    translations = TranslatedFields(
        title = models.CharField(max_length=256, null=True, blank=True),
        description = models.TextField(null=True, blank=True),
        help_text = models.TextField(null=True, blank=True)
    )

    objects = QuestionManager()


class QuizToCareer(models.Model):
    quiz = models.ForeignKey('Quiz')
    career = models.ForeignKey('Career')
    passed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)


class Career(models.Model):
    user = models.ForeignKey(User)
    quizzes = models.ManyToManyField(Quiz, null=True, blank=True,
                                through='QuizToCareer')
    

class Student(models.Model):
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s' % self.user.username


class Teacher(models.Model):
    user = models.ForeignKey(User)
    students = models.ManyToManyField('Student', null=True, blank=True,
                                 through='StudentToTeacher')

    def __unicode__(self):
        return u'%s' % self.user.username


class StudentToTeacher(models.Model):
    student = models.ForeignKey('Student')
    teacher = models.ForeignKey('Teacher')

    
