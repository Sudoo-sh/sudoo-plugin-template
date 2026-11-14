"""Webhook alerts against the SDK's fake panel: nothing is sent over the network."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from sudoo_plugin_sdk.context import PluginContext
from sudoo_plugin_sdk.manifest import Manifest
from sudoo_plugin_sdk.plugins import Notification, NotificationChannel
from sudoo_plugin_sdk.testing import make_context

from example_webhook_alerts.plugin import WebhookAlerts

FAILED = Notification(
    event="update.failed",
    title="Update of sales-main failed",
    text="git pull: merge conflict in addons/sale/models.py",
    severity="error",
    url="https://panel.example.test/instances/sales-main",
)


class Recorder:
    def __init__(self, status: int = 200) -> None:
        self.status = status
        self.sent: list[tuple[str, dict[str, str]]] = []

    def __call__(self, url: str, body: bytes) -> int:
        self.sent.append((url, json.loads(body)))
        return self.status


def channel(manifest: Manifest, tmp_path: Path, recorder: Recorder, **settings: str) -> WebhookAlerts:
    values = {"webhook_url": "https://hooks.example.test/T000/B000/x"} | settings
    return WebhookAlerts(make_context(manifest, settings=values, data_dir=tmp_path), post=recorder)


def test_it_is_a_notification_channel(sudoo_context: PluginContext) -> None:
    plugin = WebhookAlerts(sudoo_context)
    assert isinstance(plugin, NotificationChannel)
    assert not plugin.ready  # no webhook address by default


def test_sends_a_slack_message(sudoo_manifest: Manifest, tmp_path: Path) -> None:
    recorder = Recorder()
    channel(sudoo_manifest, tmp_path, recorder).send(FAILED)
    [(url, body)] = recorder.sent
    assert url == "https://hooks.example.test/T000/B000/x"
    assert body["text"].startswith("Error: Update of sales-main failed\ngit pull: merge conflict")
    assert body["text"].endswith("https://panel.example.test/instances/sales-main")


def test_discord_format(sudoo_manifest: Manifest, tmp_path: Path) -> None:
    recorder = Recorder()
    channel(sudoo_manifest, tmp_path, recorder, payload="discord").send(FAILED)
    assert "content" in recorder.sent[0][1]


def test_below_the_minimum_severity_nothing_is_sent(sudoo_manifest: Manifest, tmp_path: Path) -> None:
    recorder = Recorder()
    plugin = channel(sudoo_manifest, tmp_path, recorder)  # default: warning and above
    plugin.send(Notification(event="job.finished", title="Backup done", text="", severity="success"))
    assert recorder.sent == []


def test_a_refusal_is_explained(sudoo_manifest: Manifest, tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="HTTP 404"):
        channel(sudoo_manifest, tmp_path, Recorder(status=404)).send(FAILED)


@pytest.mark.parametrize(
    ("settings", "message"),
    [
        ({"webhook_url": "http://hooks.example.test/x"}, "https://"),
        ({"minimum_severity": "loud"}, "Send alerts from"),
        ({"payload": "teams"}, "Message format"),
    ],
)
def test_bad_settings_are_refused_at_start(
    sudoo_manifest: Manifest, tmp_path: Path, settings: dict[str, str], message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        channel(sudoo_manifest, tmp_path, Recorder(), **settings)


def test_asks_only_for_outbound_network(sudoo_manifest: Manifest) -> None:
    assert sudoo_manifest.permissions == ["network.outbound"]
