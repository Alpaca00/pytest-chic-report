import json
import ssl
import urllib.request as urllib
from datetime import datetime
from typing import Optional, Literal

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


class ClientMessenger:
    def __init__(
        self,
        slack_webhook: Optional[str] = None,
        teams_webhook: Optional[str] = None,
        ssl_verify: bool = False,
    ):
        self.slack_webhook = slack_webhook
        self.teams_webhook = teams_webhook
        self.ssl_verify = ssl_verify
        self.timeout = 60

    def slack_send_message(
        self,
        message: str,
        colored: Literal["green", "red", "yellow"],
        whois: str = "Anonymous",
    ):
        """Send a Slack message to a channel via a webhook.

        :message: String containing Slack message
        :colored: String containing color of the message, e.g. "green", "red", "yellow"
        :whois: String containing the name of the sender
        """
        if colored == "green":
            color = "#36a64f"
        elif colored == "red":
            color = "#a8323a"
        else:
            color = "#f4faa2"
        attachments = {
            "attachments": [
                {
                    "color": color,
                    "text": message,
                    "fallback": "This message is colored.",
                    "footer": "Sent by " + whois,
                    "ts": datetime.now().timestamp(),
                }
            ]
        }
        payload = json.dumps(attachments)
        urllib.urlopen(
            url=self.slack_webhook,
            data=payload.encode("utf-8"),
            context=ctx if not self.ssl_verify else None,
            timeout=self.timeout,
        )

    def teams_send_message(self, message: str):
        """Send a Teams message to a channel via a webhook.

        :message: String containing Teams message
        """
        payload = json.dumps({"text": message})
        urllib.urlopen(
            url=self.teams_webhook,
            data=payload.encode("utf-8"),
            context=ctx if not self.ssl_verify else None,
            timeout=self.timeout,
        )
