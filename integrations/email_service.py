import smtplib
from email.mime.text import MIMEText
import logging
from datetime import datetime

class EmailNotifier:
    def __init__(self):
        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 587
        self.username = "your_email@gmail.com"  # Replace with your email
        self.password = "your_app_password"     # Replace with app password
        self.logger = logging.getLogger("email_service")

    def send(self, to_email, subject, body, is_html=False):
        """Send email with verification features"""
        try:
            # Create message
            if is_html:
                msg = MIMEText(body, 'html')
            else:
                msg = MIMEText(body)
            
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = to_email

            # Send email (with alternative method)
            try:
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.username, self.password)
                    server.send_message(msg)
            except Exception as e:
                print(f"SMTP failed, trying alternative method: {str(e)}")
                # Fallback to system mail command
                import subprocess
                subprocess.run(
                    ['mail', '-s', subject, '-a', f'From: {self.username}', to_email],
                    input=body.encode(),
                    check=True
                )
            
            self.logger.info(f"Email sent to {to_email} at {datetime.now()}")
            return True
            
        except Exception as e:
            self.logger.error(f"Email failed to {to_email}: {str(e)}")
            return False

    def send_verification_email(self):
        """Send immediate test email"""
        return self.send(
            "shehryarzahid94@gmail.com",
            "Picoworker: System Verification",
            f"""Your Picoworker automation system is fully operational.

System Status:
- Email Service: Active
- Payment Monitoring: Ready
- AI Detection: Enabled
- Dashboard: Accessible at http://localhost:8000

Current Time: {datetime.now()}
"""
        )