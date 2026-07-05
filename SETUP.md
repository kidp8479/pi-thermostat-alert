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
└── .env
```

## 2. Setup environment

### On the RPi:
```bash
cd pi-thermostat-alert
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Configure API keys

### OpenWeatherMap API:
1. Go to https://openweathermap.org/api
2. Create a free account
3. Copy your API key
4. Add it to `.env` with your latitude/longitude

### Discord Webhook:
1. Create a Discord server (or use an existing one)
2. Create a #alerts channel
3. Settings → Integrations → Webhooks
4. Create a webhook and copy the URL
5. Add the URL to `.env`

## 4. Test with mock (before receiving the sensor)
```bash
python3 main.py
```

This will read mock temperatures and send to Discord. Verify it works.

## 5. When you receive the DHT22

### GPIO wiring:
```
DHT22   →   RPi
VCC     →   Pin 2 (5V)
GND     →   Pin 6 (GND)
Data    →   Pin 11 (GPIO17)
```

### In the code:
Change in `main.py`:
```python
monitor = TemperatureMonitor(use_mock_sensor=False)
```

## 6. Run continuously (systemd service)

Create `/etc/systemd/system/temp-monitor.service`:
```ini
[Unit]
Description=Temperature Monitor
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/pi-thermostat-alert
ExecStart=/home/pi/pi-thermostat-alert/venv/bin/python3 /home/pi/pi-thermostat-alert/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable temp-monitor
sudo systemctl start temp-monitor
sudo systemctl status temp-monitor
```

Logs:
```bash
tail -f /tmp/pi-thermostat-alert.log
```