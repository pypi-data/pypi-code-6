from kotti.resources import Content
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import String
from sqlalchemy import Boolean

from kotti_quiz import _
from kotti.interfaces import IDefaultWorkflow
from zope.interface import implements


class Quiz(Content):
    """Quiz Content type."""
    implements(IDefaultWorkflow)

    id = Column(Integer, ForeignKey('contents.id'), primary_key=True)

    def check_answers(self, questions, answers):
        sumtotal = 0
        sumcorrect = 0
        questioncorrect = {
            question.name: [False, [0, 0]] for question in questions}
        for question in questions:
            if question.question_type == "text":
                sumtotal += 1
                questioncorrect[question.name][1][1] += 1
                if question.name in answers and len(
                        answers[question.name]) > 0:
                    if question.correct_answer == answers[question.name][0]:
                        questioncorrect[question.name][0] = True
                        questioncorrect[question.name][1][0] += 1
                        sumcorrect += 1
            else:
                answerchoices = question.children
                # import pdb; pdb.set_trace()
                for answerchoice in answerchoices:
                    if answerchoice.correct is True:
                        sumtotal += 1
                        questioncorrect[question.name][1][1] += 1
                        if question.question_type == "radio":
                            if question.name in answers and len(
                                    answers[question.name]) > 0:
                                if answerchoice.title == answers[
                                        question.name][0]:
                                    sumcorrect += 1
                                    questioncorrect[question.name][0] = True
                                    questioncorrect[question.name][1][0] = 1
                        else:
                            if question.name in answers:
                                for choice in answers[question.name]:
                                    # import pdb; pdb.set_trace()
                                    if answerchoice.title == choice:
                                        sumcorrect += 1
                                        questioncorrect[
                                            question.name][0] = True
                                        questioncorrect[
                                            question.name][1][0] += 1
        return {
            "questioncorrect": questioncorrect,
            "sumtotal": sumtotal,
            "sumcorrect": sumcorrect
        }

    type_info = Content.type_info.copy(
        name=u'Quiz',
        title=_(u'Quiz'),
        add_view=u'add_quiz',
        addable_to=[u'Document'],
        )


class Question(Content):
    """Question Content type."""

    id = Column(Integer, ForeignKey('contents.id'), primary_key=True)
    correct_answer = Column(Unicode(256))
    question_type = Column(String())

    # change the type info to your needs
    type_info = Content.type_info.copy(
        name=u'Question',
        title=_(u'Question'),
        add_view=u'add_question',
        addable_to=[u'Quiz'],
        )


class Answer(Content):
    """Answer Content type."""

    id = Column(Integer, ForeignKey('contents.id'), primary_key=True)
    correct = Column(Boolean())

    type_info = Content.type_info.copy(
        name=u'Answer',
        title=_(u'Answer'),
        add_view=u'add_answer',
        addable_to=[u'Question'],
        )
