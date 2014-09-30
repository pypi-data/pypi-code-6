from pytest import raises
from pyramid.httpexceptions import HTTPFound


def test_question_view(dummy_request):

    from kotti_quiz.resources import Question
    from kotti_quiz.resources import Answer
    from kotti_quiz.views.quiz import QuestionView
    context = Question()
    view = QuestionView(context, dummy_request)
    # answers should be empty
    result = view.view_question()
    assert "answers" in result
    assert len(result["answers"]) == 0
    # create an answer and check if it is in the result
    context["a1"] = Answer()
    result = view.view_question()
    assert "answers" in result
    assert len(result["answers"]) == 1


def test_add_answer_to_text(quiz, dummy_request):

    from kotti_quiz.views.quiz import AnswerAddForm

    view = AnswerAddForm(quiz["question1"], dummy_request)
    with raises(HTTPFound):
        view.save_success({})
    assert dummy_request.session.pop_flash('error') == [
        u'Cannot add answer to freetext question']


def test_add_rightanswer_to_singlechoice(quiz, dummy_request):

    from kotti_quiz.views.quiz import AnswerAddForm

    view = AnswerAddForm(quiz["question2"], dummy_request)
    with raises(HTTPFound):
        view.save_success({'correct': True})
    assert dummy_request.session.pop_flash('error') == [
        u'Question already has a correct answer']


def test_add_wronganswer_to_singlechoice(quiz, dummy_request):

    from kotti_quiz.views.quiz import AnswerAddForm

    view = AnswerAddForm(quiz["question2"], dummy_request)
    view.save_success({'correct': False, 'title': 'test'})
    assert dummy_request.session.pop_flash('success') == [u'Item was added.']
