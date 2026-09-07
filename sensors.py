import logging
import time

from config import DHT22_PIN, SENSOR_SETTLE_SECONDS

logger = logging.getLogger(__name__)

MOCK_READING = {"temperature": 24.5, "humidity": 45.0}


class TemperatureSensor:
    """DHT22 reader. With use_mock=True it returns a fixed reading and needs
    neither hardware nor the Blinka stack (which only installs on the Pi)."""

    def __init__(self, use_mock: bool = False) -> None:
        self.use_mock = use_mock
        self._dht = None
        self._last_read_time = 0.0

        if not use_mock:
            # Imported here so the module stays importable off-Pi (tests, CI).
            import adafruit_dht
            import board

            self._dht = adafruit_dht.DHT22(getattr(board, DHT22_PIN))

    def read(self) -> dict[str, float] | None:
        """Return {"temperature", "humidity"} in Celsius / %, or None on failure."""
        if self.use_mock:
            return dict(MOCK_READING)

        elapsed = time.time() - self._last_read_time
        if elapsed < SENSOR_SETTLE_SECONDS:
            time.sleep(SENSOR_SETTLE_SECONDS - elapsed)

        try:
            temperature = self._dht.temperature
            humidity = self._dht.humidity
            if temperature is None or humidity is None:
                raise RuntimeError("DHT22 returned no value")
        except RuntimeError as e:
            # RuntimeError is the DHT library's normal "checksum failed, retry"
            # signal, not a fatal error.
            logger.warning("DHT22 read failed: %s", e)
            return None

        self._last_read_time = time.time()
        return {"temperature": temperature, "humidity": humidity}

    def cleanup(self) -> None:
        if self._dht is not None:
            self._dht.exit()
