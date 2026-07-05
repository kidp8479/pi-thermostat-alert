# RPi Thermostat Alert

Monitor indoor and outdoor temperature on Raspberry Pi 5. Sends Discord alerts when outdoor temperature exceeds indoor temperature, so you know when to open windows during heatwaves.

## Setup

See SETUP.md for detailed instructions.

## Quick Start

```bash
git clone git@github.com:kidp8479/pi-thermostat-alert.git
cd pi-thermostat-alert
python3 -m venv venv
source venv/bin/activate
sudo apt install libgpiod2 python-3-lgpio
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python3 main.py
```
