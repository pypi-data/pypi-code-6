pytest_plugins = "kotti"

from pytest import fixture


@fixture
def quiz(db_session, root):

    from kotti_quiz.resources import Question
    from kotti_quiz.resources import Answer
    from kotti_quiz.resources import Quiz

    context = root["quiz"] = Quiz()

    question1 = context["question1"] = Question()
    question1.question_type = "text"
    question1.correct_answer = "testright"

    question2 = context["question2"] = Question()
    question2.question_type = "radio"
    question2["a1"] = Answer()
    question2["a1"].correct = True
    question2["a1"].title = "testright"
    question2["a2"] = Answer()
    question2["a2"].correct = False
    question2["a2"].title = "testwrong"

    question3 = context["question3"] = Question()
    question3.question_type = "checkbox"
    question3["a1"] = Answer()
    question3["a1"].correct = True
    question3["a1"].title = "testright1"
    question3["a2"] = Answer()
    question3["a2"].correct = True
    question3["a2"].title = "testright2"
    question3["a3"] = Answer()
    question3["a3"].correct = False
    question3["a3"].title = "testwrong"

    db_session.flush()
    return context
