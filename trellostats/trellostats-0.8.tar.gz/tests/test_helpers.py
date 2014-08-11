import pytest
from mock import Mock, MagicMock, patch

import trellostats
from trellostats.reports import render_text, render_html, get_env
from trellostats.helpers import cycle_time, init_db
from trellostats.trellostats import TrelloStatsException
from peewee import SqliteDatabase


def test_cycle_time():
	mock_ts, mock_board, mock_done = Mock(), Mock(), Mock()
	cycle_time(mock_ts, mock_board, mock_done)
	assert mock_ts.get_list_from_name.called_once_with(mock_done)
	assert mock_ts.get_list_data.called_once_with(Mock())
	assert mock_ts.cycle_time.called_once_with(MagicMock())


def test_cycle_time_handles_failure():
	with pytest.raises(TrelloStatsException):
		mock_ts, mock_board, mock_done = Mock(), Mock(), Mock()
		mock_ts.get_list_id_from_name.side_effect = TrelloStatsException
		cycle_time(mock_ts, mock_board, mock_done)


def test_init_db():
	mock_db_proxy = Mock()
	init_db(mock_db_proxy)
	assert mock_db_proxy.called_once_with(SqliteDatabase('snapshots.db'))
