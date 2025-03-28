import requests
import logging
from datetime import datetime

class MailgunNotifier:
    def __init__(self):
        # Get your free API key from mailgun.com
        self.api_key = "your-mailgun-api-key"
        self.domain = "yourdomain.mailgun.org"
        self.from_email = "picoworker@yourdomain.mailgun.org"
        self.logger = logging.getLogger("mailgun_service")

    def send(self, to_email, subject, body):
        """Send email via Mailgun API"""
        try:
            response = requests.post(
                f"https://api.mailgun.net/v3/{self.domain}/messages",
                auth=("api", self.api_key),
                data={
                    "from": f"Picoworker System <{self.from_email}>",
                    "to": to_email,
                    "subject": subject,
                    "text": body
                }
            )
            response.raise_for_status()
            self.logger.info(f"Email sent to {to_email}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            return False

    def send_verification(self):
        """Send immediate test email"""
        return self.send(
            "shehryarzahid94@gmail.com",
            "Picoworker: System Active",
            f"""Your Picoworker automation system is now monitoring:

Easypaisa Account: +923249579762
Notification Email: shehryarzahid94@gmail.com
Start Time: {datetime.now()}

You will receive email alerts for every $5 received.
"""
        )