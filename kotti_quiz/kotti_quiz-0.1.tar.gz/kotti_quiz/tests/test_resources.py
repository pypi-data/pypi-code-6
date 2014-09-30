

def test_empty(quiz):

    # Test for empty input
    result = quiz.check_answers([], {})
    assert "sumtotal" in result
    assert result["sumtotal"] == 0
    assert "sumcorrect" in result
    assert result["sumcorrect"] == 0
    assert "questioncorrect" in result
    assert result["questioncorrect"] == {}


def test_textcorrect(quiz):

    # Test a textquestion with correct answer
    answers = {quiz["question1"].name: [quiz["question1"].correct_answer]}
    result = quiz.check_answers([quiz["question1"]], answers)
    assert "sumtotal" in result
    assert result["sumtotal"] == 1
    assert "sumcorrect" in result
    assert result["sumcorrect"] == 1
    assert "questioncorrect" in result
    assert result["questioncorrect"] == {
        quiz["question1"].name: [True, [1, 1]]}


def test_textincorrect(quiz):

    # Test a textquestion with incorrect answer
    answers = {quiz["question1"].name: [""]}
    result = quiz.check_answers([quiz["question1"]], answers)
    assert "sumtotal" in result
    assert result["sumtotal"] == 1
    assert "sumcorrect" in result
    assert result["sumcorrect"] == 0
    assert "questioncorrect" in result
    assert result["questioncorrect"] == {
        quiz["question1"].name: [False, [0, 1]]}


def test_radiocorrect(quiz):

    # Test a single-choice question with correct answer
    answers = {quiz["question2"].name: [quiz["question2"]["a1"].title]}
    result = quiz.check_answers([quiz["question2"]], answers)
    assert "sumtotal" in result
    assert result["sumtotal"] == 1
    assert "sumcorrect" in result
    assert result["sumcorrect"] == 1
    assert "questioncorrect" in result
    assert result["questioncorrect"] == {
        quiz["question2"].name: [True, [1, 1]]}


def test_radioincorrect(quiz):

    # Test a single-choice question with incorrect answer
    answers = {quiz["question2"].name: [quiz["question2"]["a2"].title]}
    result = quiz.check_answers([quiz["question2"]], answers)
    assert "sumtotal" in result
    assert result["sumtotal"] == 1
    assert "sumcorrect" in result
    assert result["sumcorrect"] == 0
    assert "questioncorrect" in result
    assert result["questioncorrect"] == {
        quiz["question2"].name: [False, [0, 1]]}


def test_checkboxcorrect(quiz):

    # Test a multiple-choice question with one correct answer
    answers = {
        quiz["question3"].name: [quiz["question3"]["a1"].title]}
    result = quiz.check_answers([quiz["question3"]], answers)
    assert "sumtotal" in result
    assert result["sumtotal"] == 2
    assert "sumcorrect" in result
    assert result["sumcorrect"] == 1
    assert "questioncorrect" in result
    assert result["questioncorrect"] == {
        quiz["question3"].name: [True, [1, 2]]}


def test_checkboxincorrect(quiz):

    # Test a multiple-choice question with one incorrect answer
    answers = {quiz["question3"].name: [quiz["question3"]["a3"].title]}
    result = quiz.check_answers([quiz["question3"]], answers)
    assert "sumtotal" in result
    assert result["sumtotal"] == 2
    assert "sumcorrect" in result
    assert result["sumcorrect"] == 0
    assert "questioncorrect" in result
    assert result["questioncorrect"] == {
        quiz["question3"].name: [False, [0, 2]]}
