from unittest.mock import MagicMock, patch

import pytest
import requests

from alerter import DiscordAlerter


def _ok():
    return MagicMock(raise_for_status=lambda: None)


def test_no_webhook_configured_is_a_noop():
    alerter = DiscordAlerter()
    alerter.webhook_url = None

    assert alerter.send_alert(24.0, 26.0, 2.0, "close") is False


@pytest.mark.parametrize(
    ("mode", "expected_title"),
    [("open", "🪟 Ouvre les fenêtres!"), ("close", "🪟 Ferme les fenêtres!")],
)
def test_send_alert_posts_the_embed_for_the_mode(mode, expected_title):
    alerter = DiscordAlerter()
    alerter.webhook_url = "https://discord.example/webhook"

    with patch("alerter.requests.post", return_value=_ok()) as post:
        ok = alerter.send_alert(24.0, 26.5, 2.5, mode)

    assert ok is True
    embed = post.call_args.kwargs["json"]["embeds"][0]
    assert embed["title"] == expected_title
    assert embed["fields"][2] == {"name": "Différence", "value": "+2.5°C", "inline": False}


def test_returns_false_on_request_error():
    alerter = DiscordAlerter()
    alerter.webhook_url = "https://discord.example/webhook"

    with patch("alerter.requests.post", side_effect=requests.exceptions.ConnectionError):
        ok = alerter.send_alert(24.0, 23.0, -1.0, "open")

    assert ok is False
