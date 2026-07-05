import board
import adafruit_dht
from config import DHT22_PIN
import time

class TemperatureSensor:
    def __init__(self, use_mock=False):
        self.use_mock = use_mock
        if not use_mock:
            self.dht = adafruit_dht.DHT22(board.D17)  # or your GPIO
        self.last_read_time = 0
    
    def read(self):
        """Read temperature and humidity from DHT22"""
        # DHT22 needs ~2 seconds between readings
        if time.time() - self.last_read_time < 2:
            time.sleep(2)
        
        try:
            if self.use_mock:
                return {"temperature": 24.5, "humidity": 45}
            
            temperature = self.dht.temperature
            humidity = self.dht.humidity
            
            if temperature is None or humidity is None:
                raise RuntimeError("DHT22 read failed")
            
            self.last_read_time = time.time()
            return {"temperature": temperature, "humidity": humidity}
        
        except RuntimeError as e:
            print(f"DHT22 error: {e}")
            return None
    
    def cleanup(self):
        if not self.use_mock and hasattr(self, 'dht'):
            self.dht.exit()
