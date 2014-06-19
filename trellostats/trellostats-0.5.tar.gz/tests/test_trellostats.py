import os
import sys

sys.path.insert(0, os.path.join(os.pardir, 'trellostats'))

import pytest
from mock import Mock, MagicMock, patch

import trellostats
from trellostats import TrelloStats, ACTION_URL, BOARD_URL, LIST_URL


@pytest.fixture
def ts_obj():
    mock_context = dict(app_key=Mock(), app_token=Mock(), board_id=Mock())
    return TrelloStats(mock_context)


@patch('trellostats.TrelloStats.get_lists')
def test_get_list_id_from_name_works(mock_get_lists, ts_obj):
    mock_get_lists.return_value = [{'id': 'eh23jnd2', 'name': 'Thang'}]
    list_id = ts_obj.get_list_id_from_name("Thang")
    assert list_id == 'eh23jnd2'


@patch('trellostats.TrelloStats.get_lists')
def test_get_list_id_from_name_is_none_with_nonexistent_name(mock_get_lists,
                                                             ts_obj):
    mock_get_lists.return_value = [{'id': 'eh23jnd2', 'name': 'Thang'}]
    list_id = ts_obj.get_list_id_from_name("NotThang")
    assert not list_id


@patch('requests.get')
def test_get_lists(mock_get, ts_obj):
    ts_obj.get_lists()
    mock_get.assert_called_with(BOARD_URL.format(ts_obj.board_id,
                                                          ts_obj.app_key,
                                                          ts_obj.app_token))


@patch('trellostats.requests.get')
def test_get_list_data(mock_get, ts_obj):
    ts_obj.get_list_data('listylist')
    mock_get.assert_called_with(LIST_URL.format('listylist',
                                                         ts_obj.app_key,
                                                         ts_obj.app_token))


@patch('trellostats.grequests.map')
def test_get_history_for_cards(mock_g, ts_obj):
    ts_obj._get_history_for_cards(MagicMock(spec=dict))
    assert mock_g.called


def test_repr(ts_obj):
    assert repr(ts_obj).startswith('<TrelloStats')
