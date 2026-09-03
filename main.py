#!/usr/bin/env python3

import logging
import time

from alerter import DiscordAlerter
from config import CHECK_INTERVAL, LOG_FILE, USE_MOCK_SENSOR
from sensors import TemperatureSensor
from weather import WeatherFetcher

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class TemperatureMonitor:
    def __init__(self, use_mock_sensor=USE_MOCK_SENSOR, sensor=None, weather=None, alerter=None):
        # Collaborators are injectable for tests; production passes nothing.
        self.sensor = sensor or TemperatureSensor(use_mock=use_mock_sensor)
        self.weather = weather or WeatherFetcher()
        self.alerter = alerter or DiscordAlerter()
        # Track state to avoid duplicate alerts: "open", "close", or None
        self.last_state = None

    def check_temperatures(self):
        """Read temps and trigger alerts on state change"""
        indoor_data = self.sensor.read()
        if not indoor_data:
            logger.error("Failed to read indoor temperature")
            return False

        outdoor_data = self.weather.fetch_outdoor_temp()
        if not outdoor_data:
            logger.error("Failed to fetch outdoor temperature")
            return False

        indoor_temp = indoor_data["temperature"]
        outdoor_temp = outdoor_data["temperature"]
        difference = outdoor_temp - indoor_temp

        logger.info(
            "Indoor: %.1f°C | Outdoor: %.1f°C | Diff: %+.1f°C",
            indoor_temp,
            outdoor_temp,
            difference,
        )

        # Open windows when outdoor < indoor (cooler outside)
        if outdoor_temp < indoor_temp and self.last_state != "open":
            logger.warning("OPEN: outdoor %.1f°C < indoor %.1f°C", outdoor_temp, indoor_temp)
            self.alerter.send_alert(indoor_temp, outdoor_temp, difference, "open")
            self.last_state = "open"

        # Close windows when outdoor > indoor (hotter outside)
        elif outdoor_temp > indoor_temp and self.last_state != "close":
            logger.warning("CLOSE: outdoor %.1f°C > indoor %.1f°C", outdoor_temp, indoor_temp)
            self.alerter.send_alert(indoor_temp, outdoor_temp, difference, "close")
            self.last_state = "close"

        return True

    def run(self):
        """Main loop: check temperatures at regular intervals"""
        logger.info("Temperature monitor started")

        try:
            while True:
                self.check_temperatures()
                time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            logger.info("Monitor stopped")
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            self.sensor.cleanup()


if __name__ == "__main__":
    # Sensor mode comes from USE_MOCK_SENSOR in the environment.
    monitor = TemperatureMonitor()
    monitor.run()
