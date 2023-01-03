#### pytest-summary

A pytest plugin to send optional summary to messengers and printing optional summary of tests in the terminal.

#### Installation
> pip install pytest-summary


**Available pytest-summary options:**
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

**Supported messengers:** `Slack`
    
**Short summary**

<img src="./docs/images/pytest-summary-slack.png" width="400" height="200">

**Summary with failed list tests**
    
<img src="./docs/images/pytest-summary-optional-slack.png" width="400" height="500">



**Printing summary in the terminal**

**Short summary**
<img src="./docs/images/pytest-summary-stdout.png" width="500" height="200">

**Summary with failed list tests**
<img src="./docs/images/pytest-summary-optional.png" width="300" height="200">

**Summary with all tests**
<img src="./docs/images/pytest-summary-optional-all.png" width="300" height="400">
