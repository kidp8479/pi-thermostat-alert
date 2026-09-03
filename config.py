"""Runtime configuration, read once from the environment (.env)."""

import os

from dotenv import load_dotenv

load_dotenv()


def _env_bool(name, default):
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name, default):
    raw = os.getenv(name)
    return int(raw) if raw else default


# Sensor
USE_MOCK_SENSOR = _env_bool("USE_MOCK_SENSOR", False)
DHT22_PIN = os.getenv("DHT22_PIN", "D17")  # Blinka board pin name (GPIO17)
SENSOR_SETTLE_SECONDS = 2.0  # DHT22 needs ~2s between reads

# Monitor loop
CHECK_INTERVAL = _env_int("CHECK_INTERVAL", 600)

# OpenWeatherMap
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_LAT = os.getenv("WEATHER_LAT", "48.8566")  # Default: Paris
WEATHER_LON = os.getenv("WEATHER_LON", "2.3522")

# Discord
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Logging
LOG_FILE = os.getenv("LOG_FILE", "/tmp/pi-thermostat-alert.log")
