
import pytest

def test_load( te, std_te_input, std_te_tasks ):
    assert te.load(std_te_input) == std_te_tasks


@pytest.fixture
def existing_h4_input():
    return ".. JIRA-1234\n# test subtask *assignee*\nh5. h5 task *assignee*"

def test_load__existing_h4_task(te, existing_h4_input):
    assert te.load(existing_h4_input) == [{ 'markup': '..', 'issue_key': 'JIRA-1234', 'line_number': 1 },
        {'assignee': 'assignee', 'line_number': 2, 'markup': '#', 'summary': 'test subtask'},
        {'assignee': 'assignee', 'line_number': 3, 'markup': 'h5.', 'summary': 'h5 task'}]

