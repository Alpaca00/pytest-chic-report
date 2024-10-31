def prepare_addoption(parser):  # noqa
    """Prepare the command line options for the pytest command."""
    parser.addoption(
        "--summary",
        dest="summary",
        action="store_true",
        default=True,
        help="Print a summary in the terminal.",
    )
    parser.addoption(
        "--verify-ssl",
        dest="ssl_verify",
        action="store_true",
        default=False,
        help="Enable TLS certificate verification.",
    )
    parser.addoption(
        "--slack-webhook",
        dest="slack_webhook",
        action="store",
        default=None,
        help="Send a Slack summary message to a channel via the webhook URL.",
    )
    parser.addoption(
        "--teams-webhook",
        dest="teams_webhook",
        action="store",
        default=None,
        help="Send a Teams summary message to a channel via the webhook URL.",
    )
    parser.addoption(
        "--include-failed",
        dest="include_failed",
        action="store_true",
        default=False,
        help="Include a template of failed tests in the message.",
    )
    parser.addoption(
        "--include-errors",
        dest="include_errors",
        action="store_true",
        default=False,
        help="Include a template of error tests in the message.",
    )
    parser.addoption(
        "--include-all-tests",
        dest="include_all_tests",
        action="store_true",
        default=False,
        help="Include a template of all tests in the message.",
    )
