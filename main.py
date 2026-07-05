#!/usr/bin/env python3

import time
import logging
from datetime import datetime
from sensors import TemperatureSensor
from weather import WeatherFetcher
from alerter import DiscordAlerter
from config import CHECK_INTERVAL, ALERT_THRESHOLD

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/pafroidu/projects/pi-thermostat-alert/temp_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TemperatureMonitor:
    def __init__(self, use_mock_sensor=True):
        self.sensor = TemperatureSensor(use_mock=use_mock_sensor)
        self.weather = WeatherFetcher()
        self.alerter = DiscordAlerter()
        self.alert_active = False
    
    def check_temperatures(self):
        """Read temperatures and check if alert should be triggered"""
        # Read indoor temperature
        indoor_data = self.sensor.read()
        if not indoor_data:
            logger.error("Failed to read indoor temperature")
            return False
        
        indoor_temp = indoor_data["temperature"]
        
        # Read outdoor temperature
        outdoor_data = self.weather.fetch_outdoor_temp()
        if not outdoor_data:
            logger.error("Failed to fetch outdoor temperature")
            return False
        
        outdoor_temp = outdoor_data["temperature"]
        
        # Calculate difference
        difference = outdoor_temp - indoor_temp
        
        logger.info(f"Indoor: {indoor_temp:.1f}°C | Outdoor: {outdoor_temp:.1f}°C | Diff: {difference:+.1f}°C")
        
        # Simple logic: alert if outdoor > indoor
        if outdoor_temp > indoor_temp and not self.alert_active:
            # Trigger alert
            logger.warning(f"ALERT: Outdoor ({outdoor_temp:.1f}°C) > Indoor ({indoor_temp:.1f}°C)")
            self.alerter.send_alert(indoor_temp, outdoor_temp, difference)
            self.alert_active = True
        
        elif outdoor_temp <= indoor_temp and self.alert_active:
            # Reset alert
            logger.info("Alert condition cleared")
            self.alerter.send_info("Alerte désactivée", indoor_temp, outdoor_temp)
            self.alert_active = False
        
        return True
    
    def run(self):
        """Main loop"""
        logger.info("Temperature monitor started")
        logger.info(f"Check interval: {CHECK_INTERVAL}s - Alert when outdoor > indoor")
        
        try:
            while True:
                self.check_temperatures()
                time.sleep(CHECK_INTERVAL)
        
        except KeyboardInterrupt:
            logger.info("Monitor stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            self.sensor.cleanup()

if __name__ == "__main__":
    # Use use_mock_sensor=True for testing without DHT22
    # Change to use_mock_sensor=False when you have the hardware
    monitor = TemperatureMonitor(use_mock_sensor=False)
    monitor.run()
