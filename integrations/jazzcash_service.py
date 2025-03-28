import requests
import hashlib
import json
from datetime import datetime, timedelta
import logging
import time

class JazzCashService:
    def __init__(self):
        self.logger = logging.getLogger("jazzcash")
        self.load_config()
        self.setup_api_url()
        
    def load_config(self):
        try:
            with open('config/jazzcash_config.json') as f:
                self.config = json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load config: {str(e)}")
            raise

    def setup_api_url(self):
        env = self.config.get("environment", "sandbox")
        if env == "production":
            self.api_url = "https://payments.jazzcash.com.pk/ApplicationAPI/API/2.0/Payment/DoTransaction"
        else:
            self.api_url = "https://sandbox.jazzcash.com.pk/ApplicationAPI/API/2.0/Payment/DoTransaction"

    def generate_hash(self, params):
        hash_str = '|'.join(str(v) for v in params.values()) + self.config['salt']
        return hashlib.sha256(hash_str.encode()).hexdigest()

    def transfer_funds(self, amount):
        """Transfer funds to configured Easypaisa number"""
        try:
            payload = {
                "pp_Version": "2.0",
                "pp_TxnType": "MWALLET",
                "pp_Language": "EN",
                "pp_MerchantID": self.config['merchant_id'],
                "pp_Password": self.config['password'],
                "pp_TxnRefNo": f"PW{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "pp_Amount": str(int(amount * 100)),  # Convert to paisa
                "pp_TxnCurrency": "PKR",
                "pp_TxnDateTime": datetime.now().strftime("%Y%m%d%H%M%S"),
                "pp_BillReference": "picoworker",
                "pp_Description": "Funds transfer",
                "pp_TxnExpiryDateTime": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
                "pp_ReturnURL": "",
                "ppmpf_1": self.config['recipient_number'],
                "ppmpf_2": "Easypaisa",
                "ppmpf_3": "Funds Transfer"
            }
            payload["pp_SecureHash"] = self.generate_hash(payload)
            
            response = requests.post(self.api_url, json=payload, timeout=30)
            response.raise_for_status()
            
            return {
                'success': True,
                'transaction_id': payload["pp_TxnRefNo"],
                'amount': amount,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Transfer failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'amount': amount,
                'timestamp': datetime.now().isoformat()
            }

    def verify_transfer(self, transaction_id):
        """Verify a completed transaction"""
        try:
            payload = {
                "pp_Version": "2.0",
                "pp_TxnType": "MWALLET",
                "pp_Language": "EN",
                "pp_MerchantID": self.config['merchant_id'],
                "pp_Password": self.config['password'],
                "pp_TxnRefNo": transaction_id,
                "pp_RetreivalReferenceNo": transaction_id,
                "pp_TxnDateTime": datetime.now().strftime("%Y%m%d%H%M%S")
            }
            payload["pp_SecureHash"] = self.generate_hash(payload)
            
            response = requests.post(
                self.api_url.replace("DoTransaction", "InquireTransaction"),
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            self.logger.error(f"Verification failed: {str(e)}")
            return None