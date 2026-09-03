import logging
from datetime import datetime

import requests

from config import DISCORD_WEBHOOK_URL

logger = logging.getLogger(__name__)

GREEN = 65280
RED = 16711680

MODES = {
    "open": ("🪟 Ouvre les fenêtres!", "Il fait plus frais dehors", GREEN),
    "close": ("🪟 Ferme les fenêtres!", "Il fait plus chaud dehors", RED),
}


def _field(name, value, inline=True):
    return {"name": name, "value": value, "inline": inline}


class DiscordAlerter:
    def __init__(self):
        self.webhook_url = DISCORD_WEBHOOK_URL

    def send_alert(self, indoor_temp, outdoor_temp, difference, mode):
        """Send alert: mode = 'open' (cooler outside) or 'close' (hotter outside)"""
        if not self.webhook_url:
            logger.warning("Discord webhook URL not configured")
            return False

        title, description, color = MODES[mode]
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "fields": [
                _field("Température intérieure", f"{indoor_temp:.1f}°C"),
                _field("Température extérieure", f"{outdoor_temp:.1f}°C"),
                _field("Différence", f"{difference:+.1f}°C", inline=False),
                _field("Heure", datetime.now().strftime("%H:%M:%S"), inline=False),
            ],
        }

        try:
            response = requests.post(self.webhook_url, json={"embeds": [embed]}, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("Discord alert error: %s", e)
            return False

        logger.info("Discord %s alert sent", mode)
        return True
