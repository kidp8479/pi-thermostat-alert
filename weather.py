import logging

import requests

from config import WEATHER_API_KEY, WEATHER_LAT, WEATHER_LON

logger = logging.getLogger(__name__)


class WeatherFetcher:
    def __init__(self) -> None:
        self.api_url = "https://api.openweathermap.org/data/2.5/weather"

    def fetch_outdoor_temp(self) -> dict[str, float] | None:
        """Fetch current outdoor temperature from OpenWeatherMap"""
        try:
            params = {
                "lat": WEATHER_LAT,
                "lon": WEATHER_LON,
                "appid": WEATHER_API_KEY,
                "units": "metric",  # Celsius
            }
            response = requests.get(self.api_url, params=params, timeout=5)
            response.raise_for_status()

            data = response.json()
            temperature = data["main"]["temp"]
            return {"temperature": temperature}

        except requests.exceptions.RequestException as e:
            logger.error("Weather API error: %s", e)
            return None
