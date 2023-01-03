## pytest-summary

A pytest plugin to send optional summary to messengers and printing optional summary of tests in the terminal.

## Installation
```
pip install pytest-summary
```
**You need require plugin in a test module or a conftest.py**
```
pytest_plugins = ["pytest_summary.plugin"]
```


#### **Available pytest-summary options:**
```
--stdout_terminal_summary > True | False
 Printing summary in the terminal.

--stdout_terminal_all_tests > True | False
 Printing name of all tests in the terminal.
 
--stdout_terminal_failed_tests > True | False
 Printing name of failed tests in the terminal.
 
--stdout_terminal_error_tests > True | False
 Printing name of error tests in the terminal.
 
--ssl_verify > True | False
 Set the TLS certificate verification.
 
--slack_webhook_id > Incoming WebHooks type of string
 Send a Slack message of summary to a channel via a webhook.
 
--messenger_extra_template_of_failed_tests > True | False
 Add extra template of failed list tests to Slack message.
 
--messenger_extra_template_of_error_tests > True | False
 Add extra template of error list tests to Slack message.
 
--messenger_extra_template_of_all_tests > True | False
 Add extra template of all tests list tests to Slack message.
```
    
#### **Short summary in the Slack**

<img src="./docs/images/pytest-summary-slack.png" width="400" height="200">

#### **Short summary in the terminal**

<img src="./docs/images/pytest-short-summary-terminal.png" width="400" height="300">

#### **The link to additional informations** [here](./docs/details.md)
