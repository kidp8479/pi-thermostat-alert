# RPi Thermostat Alert

Monitor indoor and outdoor temperature on a Raspberry Pi 5. Sends a Discord alert
on every change of state: **open the windows** when it gets cooler outside than
inside, **close them** when it gets hotter — so the house stays comfortable
during a heatwave.

## Setup

See [SETUP.md](SETUP.md) for the full Pi + systemd walkthrough.

## Quick start

```bash
git clone git@github.com:kidp8479/pi-thermostat-alert.git
cd pi-thermostat-alert
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"        # on the Pi: pip install ".[pi]"
cp .env.example .env           # then fill in your API keys
USE_MOCK_SENSOR=true python3 main.py   # runs without a DHT22 wired
```

## Configuration

All runtime config comes from the environment (`.env`); see
[.env.example](.env.example) for the full list. Notable ones:

| Variable | Default | Purpose |
| --- | --- | --- |
| `USE_MOCK_SENSOR` | `false` | Run with fixed mock readings, no hardware |
| `DHT22_PIN` | `D17` | Blinka board pin name for the sensor data line |
| `CHECK_INTERVAL` | `600` | Seconds between checks |
| `LOG_FILE` | `/tmp/pi-thermostat-alert.log` | Log file path |

## Development

```bash
make install   # venv + dev deps + pre-commit hook
make check     # ruff format --check, ruff check, pytest (same as CI)
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow.
