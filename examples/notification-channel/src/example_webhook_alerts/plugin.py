"""Webhook alerts: posts the panel's notifications to a chat's incoming webhook (sudoo.notifications).

The panel calls `send` for every notification whose event this channel wants (`events`; empty means all) while
`ready` is true. A failure raises RuntimeError with a sentence the administrator can act on; the panel retries.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from collections.abc import Callable
from typing import ClassVar
from urllib.parse import urlsplit

from sudoo_plugin_sdk import PluginContext, SudooPlugin
from sudoo_plugin_sdk.plugins import Notification

Post = Callable[[str, bytes], int]
"""post(url, JSON body) -> HTTP status. Replaced in tests, so nothing leaves the machine."""

SEVERITY_ORDER = ("info", "success", "warning", "error")
MARKS = {"info": "Info", "success": "Done", "warning": "Warning", "error": "Error"}
TIMEOUT_SECONDS = 10


class _NoRedirects(urllib.request.HTTPRedirectHandler):
    """A webhook answers directly; a redirect could send the alert (and its secret address) somewhere else."""

    def redirect_request(self, *args: object, **kwargs: object) -> None:
        return None


def post_json(url: str, body: bytes) -> int:
    request = urllib.request.Request(  # noqa: S310 - the address is checked to be https in the constructor
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json", "User-Agent": "sudoo-webhook-alerts/0.1"},
    )
    opener = urllib.request.build_opener(_NoRedirects)
    try:
        with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
            status: int = response.status
            return status
    except urllib.error.HTTPError as error:
        return error.code


class WebhookAlerts(SudooPlugin):
    """Sends alerts to a Slack-compatible or Discord webhook. Implements NotificationChannel."""

    name = "webhook-alerts"
    label = "Webhook alerts"
    events: ClassVar[frozenset[str]] = frozenset()  # every event; the severity setting filters

    def __init__(self, context: PluginContext, post: Post = post_json) -> None:
        super().__init__(context)
        self._post = post
        self.url = self.settings.string("webhook_url").strip()
        self.minimum = self.settings.string("minimum_severity", "warning")
        self.payload = self.settings.string("payload", "slack")
        if self.url and urlsplit(self.url).scheme != "https":
            raise ValueError("Webhook address must start with https://.")
        if self.minimum not in SEVERITY_ORDER:
            raise ValueError(f"Send alerts from must be one of {', '.join(SEVERITY_ORDER)}.")
        if self.payload not in ("slack", "discord"):
            raise ValueError("Message format must be slack or discord.")

    @property
    def ready(self) -> bool:
        return bool(self.url)

    def wants(self, notification: Notification) -> bool:
        return SEVERITY_ORDER.index(notification.severity) >= SEVERITY_ORDER.index(self.minimum)

    def message(self, notification: Notification) -> str:
        lines = [f"{MARKS[notification.severity]}: {notification.title}", notification.text]
        if notification.url:
            lines.append(notification.url)
        return "\n".join(line for line in lines if line)

    def body(self, notification: Notification) -> bytes:
        key = "content" if self.payload == "discord" else "text"
        return json.dumps({key: self.message(notification)}).encode()

    def send(self, notification: Notification) -> None:
        if not self.ready or not self.wants(notification):
            return
        try:
            status = self._post(self.url, self.body(notification))
        except OSError as error:
            raise RuntimeError(f"The webhook could not be reached: {error}.") from None
        if not 200 <= status < 300:
            raise RuntimeError(f"The webhook refused the alert (HTTP {status}). Check the webhook address.")

    def on_enable(self) -> None:
        if not self.ready:
            self.logger.info("Webhook alerts is on but has no webhook address yet; no alerts are sent.")
