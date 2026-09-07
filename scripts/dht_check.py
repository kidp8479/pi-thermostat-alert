"""Standalone DHT22 wiring check.

Reads the sensor straight from the pin configured in `config.DHT22_PIN` and
prints temperature/humidity every 2s. Run on the Pi with the `pi` extra
installed: `python scripts/dht_check.py`.
"""

import time

import adafruit_dht
import board

from config import DHT22_PIN

pin = getattr(board, DHT22_PIN)
print(f"Testing {DHT22_PIN} ({pin})...")

try:
    dht = adafruit_dht.DHT22(pin)
    print("DHT22 initialized successfully")
except Exception as e:
    print(f"Failed to initialize: {e}")
    raise SystemExit(1) from e

while True:
    try:
        print(f"Temp: {dht.temperature}°C, Humidity: {dht.humidity}%")
    except RuntimeError as e:
        print(f"Read error: {e}")
    time.sleep(2)
