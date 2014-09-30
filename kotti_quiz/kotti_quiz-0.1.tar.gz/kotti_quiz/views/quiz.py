# -*- coding: utf-8 -*-

"""
Created on 2014-09-22
:author: Andreas Kaiser (disko)
"""

import colander
from kotti.views.edit import AddFormView
from kotti.views.edit import ContentSchema
from kotti.views.edit import EditFormView
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.view import view_defaults
from deform.widget import RadioChoiceWidget

from kotti_quiz import _
from kotti_quiz.resources import Quiz
from kotti_quiz.resources import Question
from kotti_quiz.resources import Answer
from kotti_quiz.views import BaseView
from kotti_quiz.fanstatic import kotti_quiz_group


class QuizSchema(ContentSchema):
    title = colander.SchemaNode(
        colander.String(),
        title=_(u'Quiz Title'),
        )


class QuestionSchema(ContentSchema):
    title = colander.SchemaNode(
        colander.String(),
        title=_(u'Question'),
        )
    question_type = colander.SchemaNode(
        colander.String(),
        title=_(u'Question Type'),
        validator=colander.OneOf(["radio", "checkbox", "text"]),
        widget=RadioChoiceWidget(values=[
            ["radio", _("singlechoice")],
            ["checkbox", _("multiplechoice")],
            ["text", _("freetext")]])
        )
    correct_answer = colander.SchemaNode(
        colander.String(),
        title=_(u'Correct Answer'),
        missing=None,
        default=colander.null
        )


class AnswerSchema(ContentSchema):
    title = colander.SchemaNode(
        colander.String(),
        title=_(u'Answering Choice:'),
        )
    correct = colander.SchemaNode(
        colander.Bool(),
        title=_(u'Answer Type'),
        widget=RadioChoiceWidget(values=[
            [True, _("Correct Answer")],
            [False, _("Incorrect Answer")]])
        )


@view_config(name=Quiz.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt',)
class QuizAddForm(AddFormView):
    schema_factory = QuizSchema
    add = Quiz
    item_type = _(u"Quiz")


@view_config(name=Question.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt',)
class QuestionAddForm(AddFormView):
    schema_factory = QuestionSchema
    add = Question
    item_type = _(u"Question")

    def __init__(self, context, request, **kwargs):
        super(QuestionAddForm, self).__init__(context, request, **kwargs)
        kotti_quiz_group.need()


@view_config(name=Answer.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt',)
class AnswerAddForm(AddFormView):
    schema_factory = AnswerSchema
    add = Answer
    item_type = _(u"Answer")

    @property
    def success_url(self):  # pragma: no cover
        return self.request.resource_url(self.context)

    def save_success(self, appstruct):
        prevanswers = self.context.children
        question_type = self.context.question_type

        if question_type == "text":
            self.request.session.flash(
                u'Cannot add answer to freetext question'.format(
                    self.context.title), 'error')
            raise HTTPFound(location=self.request.resource_url(self.context))
        elif question_type == "radio" and appstruct['correct'] is True:
            for prevanswer in prevanswers:
                if prevanswer.correct is True:
                    self.request.session.flash(
                        u'Question already has a correct answer'.format(
                            self.context.title), 'error')
                    raise HTTPFound(location=self.request.resource_url(
                        self.context))
        super(AnswerAddForm, self).save_success(appstruct)


@view_config(name='edit',
             context=Quiz, permission='edit',
             renderer='kotti:templates/edit/node.pt')
class QuizEditForm(EditFormView):
    schema_factory = QuizSchema


@view_config(name='edit',
             context=Question, permission='edit',
             renderer='kotti:templates/edit/node.pt')
class QuestionEditForm(EditFormView):
    schema_factory = QuestionSchema

    def __init__(self, context, request, **kwargs):
        super(QuestionEditForm, self).__init__(context, request, **kwargs)
        kotti_quiz_group.need()


@view_config(name='edit',
             context=Answer, permission='edit',
             renderer='kotti:templates/edit/node.pt')
class AnswerEditForm(EditFormView):
    schema_factory = AnswerSchema


@view_defaults(context=Quiz, permission="view")
class QuizView(BaseView):
    """View for Quiz Content Type"""

    @view_config(name="view",
                 request_method='GET',
                 renderer='kotti_quiz:templates/quizview.pt')
    def view_quiz(self):
        return {}  # pragma: no cover

    @view_config(name='view',
                 request_method='POST',
                 renderer='kotti_quiz:templates/checkview.pt')
    def check_answers(self):  # pragma: no cover
        questions = self.context.children
        answers = {question.name: self.request.POST.getall(
            question.name) for question in questions}
        results = self.context.check_answers(questions, answers)

        return {
            'questions': questions,
            'questioncorrect': results["questioncorrect"],
            'sumtotal': results["sumtotal"],
            'sumcorrect': results["sumcorrect"],
        }


@view_defaults(context=Question)
class QuestionView(BaseView):
    """View for Question Content Type"""

    @view_config(name="view", permission="view",
                 renderer='kotti_quiz:templates/questionview.pt')
    def view_question(self):
        answers = self.context.values()
        return {
            'answers': answers,
        }


@view_defaults(context=Answer)
class AnswerView(BaseView):
    """View for Answer Content Type"""

    @view_config(name="view", permission="view",
                 renderer='kotti_quiz:templates/answerview.pt')
    def view_answer(self):
        return {}  # pragma: no cover
