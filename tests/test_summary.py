import time
import platform as os_

import pytest
from unittest.mock import MagicMock, patch

from pcr.client_http import ClientMessenger
from pcr.plugin import SuiteSummary, ReportMessenger


@pytest.fixture
def mock_terminal_reporter():
    """Mock the terminal reporter."""
    mock_reporter = MagicMock()
    mock_reporter.stats = {
        "passed": [MagicMock(nodeid="test_passed")],
        "failed": [MagicMock(nodeid="test_failed")],
        "skipped": [],
        "error": [],
        "xfailed": [],
        "xpassed": [],
    }
    mock_reporter._sessionstarttime = time.time() - 10  # noqa
    return mock_reporter


@pytest.fixture
def mock_config():
    """Mock the pytest config."""
    config = MagicMock()
    config.option.summary = True
    config.option.slack_webhook = "https://hook-ss/slack"
    config.option.teams_webhook = "https://hook-tt/teams"
    config.option.include_all_tests = True
    config.option.include_failed = True
    config.option.include_errors = False
    config.option.ssl_verify = False
    return config


def test_suite_summary(mock_terminal_reporter):
    """Test the SuiteSummary class."""
    summary = SuiteSummary(mock_terminal_reporter)
    assert summary.stats["passed"] == 1
    assert summary.stats["failed"] == 1
    assert summary.total == 2
    assert summary.duration >= 0
    assert summary.os_platform == os_.platform()
    assert summary.colored == "red"


def test_report_messenger_send_messages(mock_config, mock_terminal_reporter):
    """Test sending messages with ReportMessenger."""
    messenger = ReportMessenger(
        mock_config, mock_terminal_reporter, SuiteSummary(mock_terminal_reporter)
    )

    with patch.object(
        ClientMessenger, "slack_send_message"
    ) as mock_slack_send, patch.object(
        ClientMessenger, "teams_send_message"
    ) as mock_teams_send:
        messenger.send_messages()

        mock_slack_send.assert_called_once()
        mock_teams_send.assert_called_once()
