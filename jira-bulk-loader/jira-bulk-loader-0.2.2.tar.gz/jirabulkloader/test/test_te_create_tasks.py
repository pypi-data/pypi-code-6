
import pytest
from mock import MagicMock, call

def test_load( te, std_te_input, std_te_tasks ):
    assert te.load(std_te_input) == std_te_tasks


@pytest.fixture
def existing_h5_task():
    return [
        {'markup': '...', 'issue_key': 'JIRA-1234', 'description': 'line1\nline2', 'line_number': 3}, \
        {'assignee': 'assignee', 'markup': '#', 'summary': 'sub-task', 'line_number': 4},
    ]

def test_create_subtasks_for_existing_h5_task(monkeypatch, te, existing_h5_task, dry_run_key):
    te.create_issue = MagicMock()
    te.create_issue.return_value = dry_run_key
    te.update_issue_desc = MagicMock()
    te.update_issue_desc.return_value = dry_run_key

    assert te.create_tasks(existing_h5_task) == "... JIRA-1234\nline1\nline2\n# sub-task ({0})".format(dry_run_key)
    assert te.create_issue.call_args_list == [call({'issuetype': 'Sub-task', 'assignee': 'assignee', 'markup': '#', \
            'parent' : 'JIRA-1234', 'summary': 'sub-task', 'line_number': 4 })]
    assert te.update_issue_desc.call_args_list == [call('JIRA-1234', u'line1\nline2\n# sub-task (DRYRUN-1234)')]


@pytest.fixture
def existing_h4_task():
    return [
        {'markup': '..', 'issue_key': 'JIRA-1234', 'line_number': 3}, \
        {'assignee': 'assignee', 'markup': '#', 'summary': 'sub-task', 'line_number': 4},
    ]

def test_create_subtasks_for_existing_h4_task(monkeypatch, te, existing_h4_task, dry_run_key):
    te.create_issue = MagicMock()
    te.create_issue.return_value = dry_run_key
    te.update_issue_desc = MagicMock()
    te.update_issue_desc.return_value = dry_run_key

    assert te.create_tasks(existing_h4_task) == ".. JIRA-1234\n# sub-task ({0})".format(dry_run_key)
    assert te.create_issue.call_args_list == [call({'issuetype': 'Sub-task', 'assignee': 'assignee', 'markup': '#', \
            'parent' : 'JIRA-1234', 'summary': 'sub-task', 'line_number': 4 })]



