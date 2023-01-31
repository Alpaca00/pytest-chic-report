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
        self,
        slack_webhook: Optional[str] = None,
        teams_webhook: Optional[str] = None,
        ssl_verify: bool = False
    ):
        self.slack_webhook = slack_webhook
        self.teams_webhook = teams_webhook
        self.ssl_verify = ssl_verify
        self.timeout = 60

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
            url=self.slack_webhook,
            data=payload.encode("utf-8"),
            context=ctx if not self.ssl_verify else None,
            timeout=self.timeout,
        )

    def teams_send_message(self, message: str) -> None:
        """Send a Teams message to a channel via a webhook.

        :payload: String containing Teams message
        :return: None
        """
        payload = json.dumps({"text": message})
        urllib.request.urlopen(
            url=self.teams_webhook,
            data=payload.encode("utf-8"),
            context=ctx if not self.ssl_verify else None,
            timeout=self.timeout,
        )


def pytest_addoption(parser):
    parser.addoption(
        "--terminal_short",
        action="store",
        dest="terminal_short",
        default=True,
        help="Printing summary in the terminal.",
    )
    parser.addoption(
        "--terminal_all",
        action="store",
        dest="terminal_all",
        default=False,
        help="Printing name of all tests in the terminal.",
    )
    parser.addoption(
        "--terminal_failed",
        action="store",
        dest="terminal_failed",
        default=False,
        help="Printing name of failed tests in the terminal.",
    )
    parser.addoption(
        "--terminal_errors",
        action="store",
        dest="terminal_errors",
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
        "--slack_webhook",
        action="store",
        dest="slack_webhook",
        default=None,
        help="Send a Slack message of summary to a channel via a absolute path of webhook.",
    )
    parser.addoption(
        "--teams_webhook",
        action="store",
        dest="teams_webhook",
        default=None,
        help="Send a Teams message of summary to a channel via a absolute path of webhook.",
    )
    parser.addoption(
        "--messenger_failed",
        action="store",
        dest="messenger_failed",
        default=False,
        help="Adding an additional template of failed list tests to the message.",
    )
    parser.addoption(
        "--messenger_errors",
        action="store",
        dest="messenger_errors",
        default=False,
        help="Adding an additional template of errors list tests to the message.",
    )
    parser.addoption(
        "--messenger_all",
        action="store",
        dest="messenger_all",
        default=False,
        help="Adding an additional template of list tests to the message.",
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
    summary.template_markdown = f"""> *Test suite start with platform:* {summary.os_platform}   \n> *Passed amount:*      {summary.passed}   \n> *Failed amount:*        {summary.failed}   \n> *Errors amount:*        {summary.error}   \n> *XPassed amount:*    {summary.x_passed}   \n> *Xfailed amount:*       {summary.x_failed}   \n> *Skipped amount:*     {summary.skipped}   \n> *Successful tests:*      {round(summary.passed / summary.total * 100)}  %   \n> *Test suite duration:*  {summary.duration} seconds"""
    if config.option.terminal_short:
        terminalreporter.section("Current session")
        terminalreporter.currentfspath = 1
        terminalreporter.ensure_newline()
        for key, value in summary.template_stdout.items():
            print(f"{key} {value}")
        if config.option.terminal_all:
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
        if config.option.terminal_failed:
            print(
                " "
                + extra_template(
                    terminalreporter, "failed", summary, markdown=False
                )
            )
        if config.option.terminal_errors:
            print(
                " "
                + extra_template(
                    terminalreporter, "error", summary, markdown=False
                )
            )
        print("\n")
    if slack_webhook := config.option.slack_webhook:
        message = summary.template_markdown
        prepare_msg = prepare_message(
            config=config,
            terminalreporter=terminalreporter,
            summary=summary,
            message=message,
        )
        client = ClientMessenger(
            slack_webhook=slack_webhook, ssl_verify=config.option.ssl_verify
        )
        client.slack_send_message(message=prepare_msg)

    if teams_webhook := config.option.teams_webhook:
        message = summary.template_markdown
        prepare_msg = prepare_message(
            config=config,
            terminalreporter=terminalreporter,
            summary=summary,
            message=message,
        )
        client = ClientMessenger(
            teams_webhook=teams_webhook,
            ssl_verify=config.option.ssl_verify
        )
        client.teams_send_message(message=prepare_msg)


def prepare_message(config, terminalreporter, summary, message):
    if config.option.messenger_all:
        message += extra_template(
            terminalreporter,
            ("passed", "failed", "skipped", "error", "xfailed", "xpassed"),
            summary,
        )
    if config.option.messenger_failed:
        message += extra_template(terminalreporter, "failed", summary)
    if config.option.messenger_errors:
        message += extra_template(terminalreporter, "error", summary)
    return message


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
            result += f" {name}   \n> " if markdown else f" {name}\n "
    if markdown:
        return f"""\n\n> *List of {status if isinstance(status, str) else "all"} tests:*   \n> {result}"""
    else:
        return f"""\nList of {status if isinstance(status, str) else "all"} tests:   \n {result}"""
