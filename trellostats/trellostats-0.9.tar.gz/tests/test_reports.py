import pytest
from mock import Mock, MagicMock, patch

import trellostats
from trellostats.reports import render_text, get_env


@patch('trellostats.reports.Environment')
def test_get_env(mock_env):
    get_env()
    assert mock_env.called


@patch('trellostats.reports.get_env')
def test_render_text(mock_get_env):
    render_text(MagicMock())
    assert mock_get_env.get_template.called_once_with('text.tmpl')

