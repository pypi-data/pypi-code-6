import os
import pytest
import shortuuid
from mock import Mock, MagicMock, patch


import click
from click.testing import CliRunner

import trellostats
from trellostats.cli import cli, token, resetdb, snapshot
from trellostats.trellostats import TrelloStatsException

from trellostats.settings import BOARD_URL, LIST_URL, ACTION_URL, TOKEN_URL


app_key = os.environ.get('TRELLOSTATS_APP_KEY')
app_token = os.environ.get('TRELLOSTATS_APP_TOKEN')


def test_cli_ctx_init():
	runner = CliRunner()
	result = runner.invoke(cli)
	assert result.exit_code == 0
	assert result.output.startswith("Usage")


@patch('trellostats.cli.Snapshot')
def test_reset_db(mock_snapshot):
	runner = CliRunner()
	result = runner.invoke(resetdb, input="y")
	assert result.output.startswith("Are you sure")
	assert mock_snapshot.drop_table.called_once_with(fail_silently=True)
	assert mock_snapshot.drop_table.called


@patch('trellostats.cli.TrelloStats')
def test_token(mock_ts):
	runner = CliRunner()
	result = runner.invoke(token)
	assert result.exit_code == 0
	assert mock_ts.called
