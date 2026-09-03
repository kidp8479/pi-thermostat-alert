import time

import adafruit_dht
import board

print(f"Testing GPIO17: {board.D17}")
print("Initializing DHT22...")

try:
    dht = adafruit_dht.DHT22(board.D27)
    print("DHT22 initialized successfully")
except Exception as e:
    print(f"Failed to initialize: {e}")
    exit()

while True:
    try:
        temp = dht.temperature
        humidity = dht.humidity
        print(f"Temp: {temp}°C, Humidity: {humidity}%")
    except RuntimeError as e:
        print(f"Read error: {e}")
    time.sleep(2)
