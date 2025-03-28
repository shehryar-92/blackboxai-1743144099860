import time
from datetime import datetime
from integrations.easypaisa import EasypaisaClient
from integrations.mailgun_service import MailgunNotifier
from services.jazzcash_payments import JazzCashPaymentProcessor
from datetime import datetime, timedelta

class PaymentMonitor:
    def __init__(self):
        self.client = EasypaisaClient("+923249579762")
        self.payment_processor = JazzCashPaymentProcessor()
        self.notifier = MailgunNotifier()
        self.last_threshold = 0
        self.last_transfer_time = None
        self._verify_services()
        
    def run(self):
        # Send immediate verification email
        if not self.notifier.send_verification_email():
            print("Failed to send verification email - check email configuration")
        
        # Send test payment notification
        test_msg = """TEST NOTIFICATION: Picoworker System Active

This is a test message confirming your payment automation system is working.
When your account reaches $5 increments, you'll receive similar notifications.

Dashboard: http://localhost:8000"""
        self.notifier.send("shehryarzahid94@gmail.com", 
                         "Picoworker: Test Notification", 
                         test_msg)

        while True:
            try:
                balance = self.client.check_balance()
                current_threshold = balance // 5
                
                if current_threshold > self.last_threshold:
                    amount = current_threshold * 5
                    self.notifier.send(
                        "shehryarzahid94@gmail.com",
                        f"Payment Notification: ${amount} reached",
                        f"Your account balance has reached ${amount}"
                    )
                    self.last_threshold = current_threshold
                    
            except Exception as e:
                print(f"Error at {datetime.now()}: {str(e)}")
                
            time.sleep(300)  # Check every 5 minutes

if __name__ == "__main__":
    monitor = PaymentMonitor()
    monitor.run()