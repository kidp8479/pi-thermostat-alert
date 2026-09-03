from unittest.mock import MagicMock, patch

import requests

from weather import WeatherFetcher


def _response(payload):
    return MagicMock(json=lambda: payload, raise_for_status=lambda: None)


def test_returns_temperature_from_payload():
    fetcher = WeatherFetcher()

    with patch("weather.requests.get", return_value=_response({"main": {"temp": 21.4}})):
        result = fetcher.fetch_outdoor_temp()

    assert result == {"temperature": 21.4}


def test_returns_none_on_request_error():
    fetcher = WeatherFetcher()

    with patch("weather.requests.get", side_effect=requests.exceptions.Timeout):
        result = fetcher.fetch_outdoor_temp()

    assert result is None
