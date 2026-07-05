import requests
from datetime import datetime
from config import DISCORD_WEBHOOK_URL

class DiscordAlerter:
    def __init__(self):
        self.webhook_url = DISCORD_WEBHOOK_URL
    
    def send_alert(self, indoor_temp, outdoor_temp, difference):
        """Send alert to Discord webhook"""
        if not self.webhook_url:
            print("Discord webhook URL not configured")
            return False
        
        try:
            embed = {
                "title": "🌡️ Ouvre les fenêtres!",
                "description": f"Il fait plus frais dehors qu'en dedans",
                "color": 16711680,  # Red
                "fields": [
                    {"name": "Température intérieure", "value": f"{indoor_temp:.1f}°C", "inline": True},
                    {"name": "Température extérieure", "value": f"{outdoor_temp:.1f}°C", "inline": True},
                    {"name": "Différence", "value": f"+{difference:.1f}°C", "inline": True},
                    {"name": "Heure", "value": datetime.now().strftime("%H:%M:%S"), "inline": False}
                ]
            }
            
            payload = {"embeds": [embed]}
            response = requests.post(self.webhook_url, json=payload, timeout=5)
            response.raise_for_status()
            
            print(f"Alert sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return True
        
        except requests.exceptions.RequestException as e:
            print(f"Discord alert error: {e}")
            return False
    
    def send_info(self, message, indoor_temp, outdoor_temp):
        """Send info/status message to Discord"""
        if not self.webhook_url:
            return False
        
        try:
            embed = {
                "title": "📊 Status Check",
                "description": message,
                "color": 3066993,  # Green
                "fields": [
                    {"name": "Intérieur", "value": f"{indoor_temp:.1f}°C", "inline": True},
                    {"name": "Extérieur", "value": f"{outdoor_temp:.1f}°C", "inline": True},
                ]
            }
            
            payload = {"embeds": [embed]}
            response = requests.post(self.webhook_url, json=payload, timeout=5)
            response.raise_for_status()
            return True
        
        except requests.exceptions.RequestException as e:
            print(f"Discord info error: {e}")
            return False
