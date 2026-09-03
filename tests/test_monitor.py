from unittest.mock import MagicMock

import pytest

from main import TemperatureMonitor


@pytest.fixture
def alerter():
    return MagicMock()


def build_monitor(alerter, indoor, outdoor):
    sensor = MagicMock()
    sensor.read.return_value = {"temperature": indoor, "humidity": 50}
    weather = MagicMock()
    weather.fetch_outdoor_temp.return_value = {"temperature": outdoor}
    return TemperatureMonitor(sensor=sensor, weather=weather, alerter=alerter)


def set_outdoor(monitor, outdoor):
    monitor.weather.fetch_outdoor_temp.return_value = {"temperature": outdoor}


def test_check_returns_false_when_sensor_read_fails(alerter):
    monitor = build_monitor(alerter, indoor=24.0, outdoor=25.0)
    monitor.sensor.read.return_value = None

    assert monitor.check_temperatures() is False
    alerter.send_alert.assert_not_called()


def test_check_returns_false_when_weather_fetch_fails(alerter):
    monitor = build_monitor(alerter, indoor=24.0, outdoor=25.0)
    monitor.weather.fetch_outdoor_temp.return_value = None

    assert monitor.check_temperatures() is False


def test_alerts_open_when_cooler_outside(alerter):
    monitor = build_monitor(alerter, indoor=24.0, outdoor=22.0)

    monitor.check_temperatures()

    assert monitor.last_state == "open"
    alerter.send_alert.assert_called_once_with(24.0, 22.0, -2.0, "open")


def test_alerts_close_when_hotter_outside(alerter):
    monitor = build_monitor(alerter, indoor=24.0, outdoor=27.0)

    monitor.check_temperatures()

    assert monitor.last_state == "close"
    alerter.send_alert.assert_called_once_with(24.0, 27.0, 3.0, "close")


def test_does_not_re_alert_while_state_is_unchanged(alerter):
    monitor = build_monitor(alerter, indoor=24.0, outdoor=27.0)

    monitor.check_temperatures()
    set_outdoor(monitor, 28.0)  # still hotter outside
    monitor.check_temperatures()

    alerter.send_alert.assert_called_once()


def test_re_alerts_when_state_flips(alerter):
    monitor = build_monitor(alerter, indoor=24.0, outdoor=27.0)

    monitor.check_temperatures()  # close
    set_outdoor(monitor, 21.0)
    monitor.check_temperatures()  # open

    assert monitor.last_state == "open"
    assert alerter.send_alert.call_count == 2
