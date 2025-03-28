import sys
import os
import logging
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

# Now import project modules
from integrations.mailgun_service import MailgunNotifier
from services.jazzcash_payments import JazzCashPaymentProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("verification")

def verify_email_service():
    """Test email notification service"""
    try:
        logger.info("Testing email service...")
        mailgun = MailgunNotifier()
        if mailgun.send_verification():
            logger.info("✓ Email service working")
            return True
        logger.error("✗ Email service failed")
        return False
    except Exception as e:
        logger.error(f"Email verification error: {str(e)}")
        return False

def verify_payment_service():
    """Test payment processing service"""
    try:
        logger.info("Testing payment processor with 1 PKR...")
        jazzcash = JazzCashPaymentProcessor()
        result = jazzcash.transfer_to_easypaisa(1)
        
        if result['success']:
            logger.info(f"✓ Payment successful. Transaction ID: {result['transaction_id']}")
            return True
        logger.error(f"✗ Payment failed: {result['error']}")
        return False
    except Exception as e:
        logger.error(f"Payment verification error: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Starting system verification...")
    
    email_ok = verify_email_service()
    payment_ok = verify_payment_service()
    
    if email_ok and payment_ok:
        logger.info("✅ All services verified successfully")
        exit(0)
    else:
        logger.error("❌ System verification failed")
        exit(1)