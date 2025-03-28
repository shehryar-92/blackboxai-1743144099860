import time
from datetime import datetime, timedelta
from integrations.easypaisa import EasypaisaClient
from integrations.mailgun_service import MailgunNotifier
from services.jazzcash_payments import JazzCashPaymentProcessor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("payment_automation")

class PaymentAutomation:
    def __init__(self):
        self.easypaisa = EasypaisaClient("+923249579762")
        self.jazzcash = JazzCashPaymentProcessor()
        self.notifier = MailgunNotifier()
        self.last_threshold = 0
        self.last_transfer = None
        self._verify_services()

    def _verify_services(self):
        """Verify all integrated services are working"""
        # Test email service
        if not self.notifier.send_verification():
            logger.error("Email service verification failed")
        
        # Test payment processor with 1 PKR
        test_result = self.jazzcash.transfer_to_easypaisa(1)
        if not test_result['success']:
            logger.error(f"Payment processor test failed: {test_result['error']}")
            self.notifier.send(
                "shehryarzahid94@gmail.com",
                "Picoworker: Service Verification Failed",
                f"Payment processor test failed: {test_result['error']}"
            )

    def _process_payment(self, amount):
        """Handle payment transfer with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            result = self.jazzcash.transfer_to_easypaisa(amount)
            if result['success']:
                self.notifier.send(
                    "shehryarzahid94@gmail.com",
                    f"Picoworker: {amount} PKR Transferred",
                    f"Successfully transferred {amount} PKR to your Easypaisa account\n"
                    f"Transaction ID: {result['transaction_id']}"
                )
                return True
            
            logger.warning(f"Attempt {attempt + 1} failed: {result['error']}")
            time.sleep(5)  # Wait before retry
        
        self.notifier.send(
            "shehryarzahid94@gmail.com",
            "Picoworker: Transfer Failed",
            f"Failed to transfer {amount} PKR after {max_retries} attempts"
        )
        return False

    def run(self):
        """Main monitoring loop"""
        while True:
            try:
                balance = self.easypaisa.check_balance()
                current_threshold = balance // 5
                
                # Check if we need to transfer funds
                if (current_threshold > self.last_threshold and 
                    (self.last_transfer is None or 
                     (datetime.now() - self.last_transfer) > timedelta(hours=1))):
                    
                    amount = (current_threshold - self.last_threshold) * 5
                    if self._process_payment(amount):
                        self.last_threshold = current_threshold
                        self.last_transfer = datetime.now()
                        
            except Exception as e:
                logger.error(f"Monitoring error: {str(e)}")
                self.notifier.send(
                    "shehryarzahid94@gmail.com",
                    "Picoworker: System Error",
                    f"An error occurred in payment monitoring: {str(e)}"
                )
            
            time.sleep(300)  # Check every 5 minutes

if __name__ == "__main__":
    automation = PaymentAutomation()
    automation.run()