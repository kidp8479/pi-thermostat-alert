import requests
from datetime import datetime
from config import DISCORD_WEBHOOK_URL

class DiscordAlerter:
    def __init__(self):
        self.webhook_url = DISCORD_WEBHOOK_URL
    
    def send_alert(self, indoor_temp, outdoor_temp, difference, mode):
        """Send alert: mode = 'open' (cooler outside) or 'close' (hotter outside)"""
        if not self.webhook_url:
            print("Discord webhook URL not configured")
            return False
        
        if mode == "open":
            title = "🪟 Ouvre les fenêtres!"
            description = "Il fait plus frais dehors"
            color = 65280  # Green
        else:  # close
            title = "🪟 Ferme les fenêtres!"
            description = "Il fait plus chaud dehors"
            color = 16711680  # Red
        
        try:
            embed = {
                "title": title,
                "description": description,
                "color": color,
                "fields": [
                    {"name": "Température intérieure", "value": f"{indoor_temp:.1f}°C", "inline": True},
                    {"name": "Température extérieure", "value": f"{outdoor_temp:.1f}°C", "inline": True},
                    {"name": "Différence", "value": f"{difference:+.1f}°C", "inline": False},
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
