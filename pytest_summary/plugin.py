import time
from typing import Union
import platform as os_
import json
import ssl
import urllib.request
from typing import Optional
import pytest


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


class ClientMessenger:
    def __init__(
        self, slack_webhook_id: Optional[str] = None, ssl_verify: bool = False
    ):
        self.base_url = "https://hooks.slack.com/services/"
        self.slack_webhook_id = slack_webhook_id
        self.ssl_verify = ssl_verify

    def slack_send_message(self, message: str) -> None:
        """Send a Slack message to a channel via a webhook.

        :payload: Dictionary containing Slack message, i.e. {"blocks": [dict]}
        :return: None
        """
        payload = json.dumps(
            {
                "blocks": [
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": message},
                    }
                ]
            }
        )
        urllib.request.urlopen(
            self.base_url + self.slack_webhook_id,
            data=payload.encode("utf-8"),
            context=ctx if not self.ssl_verify else None,
        )


def pytest_addoption(parser):
    parser.addoption(
        "--stdout_terminal_summary",
        action="store",
        dest="stdout_terminal_summary",
        default=True,
        help="Printing summary in the terminal.",
    )
    parser.addoption(
        "--stdout_terminal_all_tests",
        action="store",
        dest="stdout_terminal_all_tests",
        default=False,
        help="Printing name of all tests in the terminal.",
    )
    parser.addoption(
        "--stdout_terminal_failed_tests",
        action="store",
        dest="stdout_terminal_failed_tests",
        default=False,
        help="Printing name of failed tests in the terminal.",
    )
    parser.addoption(
        "--stdout_terminal_error_tests",
        action="store",
        dest="stdout_terminal_error_tests",
        default=False,
        help="Printing name of error tests in the terminal.",
    )
    parser.addoption(
        "--ssl_verify",
        action="store",
        dest="ssl_verify",
        default=False,
        help="Set the TLS certificate verification.",
    )
    parser.addoption(
        "--slack_webhook_id",
        action="store",
        dest="slack_webhook_id",
        default=None,
        help="Send a Slack message of summary to a channel via a webhook.",
    )
    parser.addoption(
        "--messenger_extra_template_of_failed_tests",
        action="store",
        dest="messenger_extra_template_of_failed_tests",
        default=False,
        help="Add extra template of failed list tests to Slack message.",
    )
    parser.addoption(
        "--messenger_extra_template_of_error_tests",
        action="store",
        dest="messenger_extra_template_of_error_tests",
        default=False,
        help="Add extra template of error list tests to Slack message.",
    )
    parser.addoption(
        "--messenger_extra_template_of_all_tests",
        action="store",
        dest="messenger_extra_template_of_all_tests",
        default=False,
        help="Add extra template of all tests list tests to Slack message.",
    )


class Summary:
    failed: int
    passed: int
    skipped: int
    error: int
    x_failed: int
    x_passed: int
    duration: Union[float, int]
    total: int
    os_platform: os_
    template_stdout: dict
    template_markdown: str
    result_is_null: str = "Nothing to found"


@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(terminalreporter, config):
    yield
    summary = Summary()
    summary.failed = len(terminalreporter.stats.get("failed", []))
    summary.passed = len(terminalreporter.stats.get("passed", []))
    summary.skipped = len(terminalreporter.stats.get("skipped", []))
    summary.error = len(terminalreporter.stats.get("error", []))
    summary.x_failed = len(terminalreporter.stats.get("xfailed", []))
    summary.x_passed = len(terminalreporter.stats.get("xpassed", []))
    summary.total = (
        summary.failed
        + summary.passed
        + summary.skipped
        + summary.error
        + summary.x_failed
        + summary.x_passed
    )
    summary.duration = round(time.time() - terminalreporter._sessionstarttime, 2)
    summary.os_platform = os_.platform()
    summary.template_stdout = {
        "Platform:": summary.os_platform,
        "Passed amount:": summary.passed,
        "Failed amount:": summary.failed,
        "Errors amount:": summary.error,
        "Xfailed amount:": summary.x_failed,
        "Xpassed amount:": summary.x_passed,
        "Skipped amount:": summary.skipped,
        "Test suite duration:": f"{summary.duration} seconds",
        "Successful tests:": f"{round(summary.passed / summary.total * 100)} %",
    }
    summary.template_markdown = f"""> *Test suite start with platform:* {summary.os_platform}\n> *Passed amount:*      {summary.passed}\n> *Failed amount:*        {summary.failed}\n> *Errors amount:*        {summary.error}\n> *XPassed amount:*    {summary.x_passed}\n> *Xfailed amount:*       {summary.x_failed}\n> *Skipped amount:*     {summary.skipped}\n> *Successful tests:*      {round(summary.passed / summary.total * 100)}  % \n> *Test suite duration:*  {summary.duration} seconds"""
    if config.option.stdout_terminal_summary:
        terminalreporter.section("Current session")
        terminalreporter.currentfspath = 1
        terminalreporter.ensure_newline()
        for key, value in summary.template_stdout.items():
            print(f"{key} {value}")
        if config.option.stdout_terminal_all_tests:
            print(
                " "
                + extra_template(
                    terminalreporter,
                    (
                        "passed",
                        "failed",
                        "skipped",
                        "error",
                        "xfailed",
                        "xpassed",
                    ),
                    summary,
                    markdown=False,
                )
            )
        if config.option.stdout_terminal_failed_tests:
            print(
                " "
                + extra_template(
                    terminalreporter, "failed", summary, markdown=False
                )
            )
        if config.option.stdout_terminal_error_tests:
            print(
                " "
                + extra_template(
                    terminalreporter, "error", summary, markdown=False
                )
            )
        print("\n")
    if slack_webhook_id := config.option.slack_webhook_id:
        message = summary.template_markdown
        client = ClientMessenger(
            slack_webhook_id=slack_webhook_id, ssl_verify=config.option.ssl_verify
        )
        if config.option.messenger_extra_template_of_all_tests:
            message += extra_template(
                terminalreporter,
                ("passed", "failed", "skipped", "error", "xfailed", "xpassed"),
                summary,
            )
        if config.option.messenger_extra_template_of_failed_tests:
            message += extra_template(terminalreporter, "failed", summary)
        if config.option.messenger_extra_template_of_error_tests:
            message += extra_template(terminalreporter, "error", summary)
        client.slack_send_message(message=message)


def extra_template(terminalreporter, status, summary, markdown=True) -> str:
    result = ""
    stats = []
    if isinstance(status, str):
        for stat in terminalreporter.stats.get(status, []):
            stats.append(f"{stat.nodeid:20}")
    else:
        for item in status:
            for stat in terminalreporter.stats.get(item, []):
                stats.append(f"{stat.nodeid:20}")
    slice_raw_path = [name.split("::")[2] for name in list(set(stats))]
    names = (
        slice_raw_path if bool(slice_raw_path) is True else summary.result_is_null
    )
    if names == summary.result_is_null:
        result = summary.result_is_null
    else:
        for name in names:
            result += f" {name}\n> " if markdown else f" {name}\n "
    if markdown:
        return f"""\n\n> *List of {status if isinstance(status, str) else "all"} tests:*\n> {result}"""
    else:
        return f"""\nList of {status if isinstance(status, str) else "all"} tests:\n {result}"""
