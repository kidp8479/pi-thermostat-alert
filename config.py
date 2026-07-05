# Configuration
import os
from dotenv import load_dotenv

load_dotenv()

# Sensors
DHT22_PIN = 17  # GPIO pin where DHT22 data line is connected
CHECK_INTERVAL = 600  # 10 minutes in seconds

# OpenWeatherMap
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_LAT = os.getenv("WEATHER_LAT", "48.8566")  # Default: Paris
WEATHER_LON = os.getenv("WEATHER_LON", "2.3522")

# Discord
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Temperature thresholds
ALERT_THRESHOLD = 0.0  # Alert if outdoor > indoor
