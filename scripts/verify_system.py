from integrations.mailgun_service import MailgunNotifier
from services.jazzcash_payments import JazzCashPaymentProcessor
import logging

logging.basicConfig(level=logging.INFO)

def test_email_service():
    print("Testing email service...")
    mailgun = MailgunNotifier()
    if mailgun.send_verification():
        print("✓ Email service working")
        return True
    print("✗ Email service failed")
    return False

def test_payment_processor():
    print("Testing payment processor...")
    jazzcash = JazzCashPaymentProcessor()
    result = jazzcash.transfer_to_easypaisa(1)  # Test with 1 PKR
    if result['success']:
        print(f"✓ Payment service working. Transaction ID: {result['transaction_id']}")
        return True
    print(f"✗ Payment service failed: {result['error']}")
    return False

if __name__ == "__main__":
    print("Starting system verification...")
    email_ok = test_email_service()
    payment_ok = test_payment_processor()
    
    if email_ok and payment_ok:
        print("✅ All services verified successfully")
        exit(0)
    else:
        print("❌ System verification failed")
        exit(1)