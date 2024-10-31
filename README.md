## pytest-chic-report


`pytest-chic-report` is a plugin for pytest that allows you to generate test result summaries in Markdown format and send them to Slack or Teams channels.

### Installation

You can install `pytest-chic-report` via pip from [PyPI](https://pypi.org/project/pytest-chic-report/).

```bash
pip install pytest-chic-report
```

### Usage

**Adding Command Line Options**

The plugin adds several command line options to customize the reports:

- `--summary:` Print a summary in the terminal (enabled by default).
- `--verify-ssl:` Enable TLS certificate verification.
- `--slack-webhook:` Specify the webhook URL for Slack to send the report.
- `--teams-webhook:` Specify the webhook URL for Teams to send the report.
- `--include-failed:` Include a template of failed tests in the message.
- `--include-errors:` Include a template of error tests in the message.
- `--include-all-tests:` Include a template of all tests in the message.

### Example Usage:

```bash
pytest --slack-webhook https://hooks.slack.com/services/XXXXX/XXXXX/XXXXX
```


### Report Format

The report is generated in Markdown format and sent to the specified channel, featuring color-coded test results:

- green: passed
- red: failed
- yellow: not run

**Example Report**

```markdown
--------- Suite Summary ---------
Passed amount: 7
Failed amount: 1
Skipped amount: 1
Xfailed amount: 4
Xpassed amount: 2
Total tests: 15
Total duration: 0.02 seconds
Successful tests: 47 %
Platform: Linux-6.8.0-47-generic-x86_64-with-glibc2.39
```

**TODO:**

- Implement xdist logic for parallel test execution.
