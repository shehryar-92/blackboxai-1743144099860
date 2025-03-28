import requests
import json
import logging
from pathlib import Path

class EmailNotifier:
    def __init__(self):
        self.logger = logging.getLogger("email_notifier")
        self.config = self._load_config()
        
    def _load_config(self):
        config_path = Path(__file__).parent.parent / "config" / "email_config.json"
        try:
            with open(config_path) as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load email config: {str(e)}")
            raise

    def send(self, to_email, subject, body):
        try:
            response = requests.post(
                f"https://api.mailgun.net/v3/{self.config['domain']}/messages",
                auth=("api", self.config["api_key"]),
                data={
                    "from": f"Picoworker System <{self.config['from_email']}>",
                    "to": to_email,
                    "subject": subject,
                    "text": body
                }
            )
            response.raise_for_status()
            return True
        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            return False

    def send_verification(self):
        return self.send(
            "shehryarzahid94@gmail.com",
            "Picoworker: System Verification",
            "Your Picoworker automation system is verifying email service."
        )