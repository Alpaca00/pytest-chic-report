import time
import platform as os_
from logging import warning

import pytest

from pcr.args_cli import prepare_addoption
from pcr.client_http import ClientMessenger


def pytest_addoption(parser):  # noqa
    """Add options to the pytest command line."""
    prepare_addoption(parser)


class SuiteSummary:
    """Handles summary calculation and storage for test results."""

    def __init__(self, stdout):
        self.stdout = stdout
        self.stats = {
            status: len(stdout.stats.get(status, []))
            for status in (
                "passed",
                "failed",
                "skipped",
                "error",
                "xfailed",
                "xpassed",
            )
        }
        self.total = sum(self.stats.values())
        self.duration = round(time.time() - stdout._sessionstarttime, 2)  # noqa
        self.os_platform = os_.platform()
        self.colored = self.__colorize()

    def __colorize(self):
        """Colorize the summary based on the test results."""
        if self.stats["failed"] or self.stats["error"]:
            return "red"
        if self.stats["passed"] == self.total:
            return "green"
        return "yellow"

    def to_dict(self):
        """Returns a dictionary representation for stdout display."""
        result = {
            f"{status.capitalize()} amount:": count
            for status, count in self.stats.items()
            if count > 0
        }
        result["Total tests:"] = self.total
        result["Total duration:"] = f"{self.duration} seconds"  # noqa
        result["Successful tests:"] = (  # noqa
            f"{round(self.stats['passed'] / self.total * 100)} %"
            if self.total
            else "0 %"
        )
        result["Platform:"] = self.os_platform  # noqa
        return result

    def to_markdown(self):
        """Returns a formatted markdown summary."""
        summary_lines = [
            f"*{key}* {value}" for key, value in self.to_dict().items()
        ]
        return "--------- Suite Summary ---------\n" + "\n".join(summary_lines)


class ReportMessenger:
    """Sends test results via configured messaging services."""

    def __init__(self, config, stdout, summary):
        self.config = config
        self.stdout = stdout
        self.summary = summary

    def send_messages(self):
        """Send messages to configured channels, e.g. Slack, Teams."""
        message = self._prepare_message()
        if slack_webhook := self.config.option.slack_webhook:
            self._send_message(slack_webhook, message, method="slack")
        if teams_webhook := self.config.option.teams_webhook:
            self._send_message(teams_webhook, message, method="teams")

    def _prepare_message(self):
        """Prepare message with extra details if requested in config."""
        message = self.summary.to_markdown()
        if self.config.option.include_all_tests:
            message += self._extra_template(
                ("passed", "failed", "skipped", "error", "xfailed", "xpassed")
            )
        if self.config.option.include_failed:
            message += self._extra_template("failed")
        if self.config.option.include_errors:
            message += self._extra_template("error")
        return message

    def _send_message(self, webhook, message, method):
        """Send the message using the appropriate method."""
        client = ClientMessenger(
            webhook, ssl_verify=self.config.option.ssl_verify
        )
        if method == "slack":
            client.slack_send_message(
                message=message, colored=self.summary.colored
            )
        elif method == "teams":
            client.teams_send_message(message=message)

    def _extra_template(self, statuses):
        """Generates a list of tests for specific statuses."""
        return ExtraTemplate(self.stdout, statuses).generate(markdown=True)


class ExtraTemplate:
    """Creates additional details for specific statuses in test summary."""

    def __init__(self, stdout, statuses):
        self.stdout = stdout
        self.statuses = statuses if isinstance(statuses, tuple) else (statuses,)

    def generate(self, markdown=True):
        """Generates formatted output of test statuses."""
        stats = [
            stat.nodeid
            for status in self.statuses
            for stat in self.stdout.stats.get(status, [])
        ]

        unique_names = list(
            set(name.split("::")[2] for name in stats if "::" in name)
        )

        if unique_names:
            result = "\n".join(
                f"{name}   \n" if markdown else f"{name}\n "
                for name in unique_names
            )
        else:
            result = "No results available."

        return (
            f"\n\n*List of {', '.join(self.statuses)} tests:*   \n {result}"
            if markdown
            else f"\nList of {', '.join(self.statuses)} tests:\n {result}"
        )


@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(terminalreporter, config):  # noqa
    yield
    summary = SuiteSummary(terminalreporter)

    if not config.getoption("dist", None):
        if config.option.summary:
            print("Current session:")
            for key, value in summary.to_dict().items():
                print(f"{key} {value}")

        messenger = ReportMessenger(config, terminalreporter, summary)
        messenger.send_messages()
    else:
        warning("Not implemented parallel execution summary.")
