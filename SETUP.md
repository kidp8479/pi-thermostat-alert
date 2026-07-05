# Setup Instructions

## 1. Clone/Copy files

Place all files in a folder on your RPi:

```
pi-thermostat-alert/
├── config.py
├── sensors.py
├── weather.py
├── alerter.py
├── main.py
├── requirements.txt
├── .env
└── .env.example
```

## 2. Setup environment

On the RPi:

```bash
cd pi-thermostat-alert
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

System dependencies (Raspberry Pi only):

```bash
sudo apt install libgpiod2 python3-lgpio
pip install lgpio
```

## 3. Configure API keys

### OpenWeatherMap API

1. Go to https://openweathermap.org/api
2. Create a free account
3. Copy your API key

### Discord Webhook

1. Create a Discord server (or use an existing one)
2. Create an #alerts channel
3. Settings → Integrations → Webhooks
4. Create a webhook and copy the URL

### Setup .env file

Copy .env.example to .env:

```bash
cp .env.example .env
nano .env
```

Fill in your OpenWeatherMap API key and Discord webhook URL.

## 4. Running the monitor

### Mock mode (for testing, no DHT22 needed)

```bash
source venv/bin/activate
python3 main.py
```

### Real mode with DHT22

Must run as root (GPIO access):

```bash
sudo /path/to/venv/bin/python3 main.py
```

Or use systemd (recommended):

```bash
sudo systemctl start temp-monitor
sudo systemctl status temp-monitor
tail -f /path/to/project/temp_monitor.log
```

To stop:

```bash
sudo systemctl stop temp-monitor
```

## 5. Setup systemd service

Create `/etc/systemd/system/temp-monitor.service`:

```ini
[Unit]
Description=Temperature Monitor
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/path/to/pi-thermostat-alert
ExecStart=/path/to/pi-thermostat-alert/venv/bin/python3 /path/to/pi-thermostat-alert/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Replace `/path/to/` with your actual paths.

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable temp-monitor
sudo systemctl start temp-monitor
```

## 6. Hardware Setup

### DHT22 wiring

```
DHT22 Module     Raspberry Pi 5
VCC (+)          Pin 2 (5V)
GND (-)          Pin 6 (GND)
Data (out)       Pin 11 (GPIO17)
```

Make sure pins are firmly inserted.

## Troubleshooting

**"DHT sensor not found"**: Check wiring, try a different GPIO pin, or update DHT22_PIN in config.py.

**Permission denied on GPIO**: Run with sudo or add user to gpio group.

**Discord webhook not working**: Verify webhook URL in .env and Discord permissions.
