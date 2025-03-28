import requests
import hashlib
import json
from datetime import datetime, timedelta
import logging
import time

class JazzCashPaymentProcessor:
    def __init__(self):
        self.logger = logging.getLogger("jazzcash")
        self.config = self._load_config()
        self.api_url = self._get_api_url()
        
    def _load_config(self):
        try:
            with open('config/jazzcash_config.json') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Config load failed: {str(e)}")
            raise

    def _get_api_url(self):
        return ("https://sandbox.jazzcash.com.pk" if self.config.get('sandbox', True) 
                else "https://payments.jazzcash.com.pk") + "/ApplicationAPI/API/2.0/Payment/DoTransaction"

    def _generate_hash(self, params):
        hash_str = '|'.join(str(v) for v in params.values()) + self.config['salt']
        return hashlib.sha256(hash_str.encode()).hexdigest()

    def transfer_to_easypaisa(self, amount):
        """Transfer funds to Easypaisa with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                payload = {
                    "pp_Version": "2.0",
                    "pp_TxnType": "MWALLET",
                    "pp_Language": "EN",
                    "pp_MerchantID": self.config['merchant_id'],
                    "pp_Password": self.config['password'],
                    "pp_TxnRefNo": f"PW{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "pp_Amount": str(int(amount * 100)),
                    "pp_TxnCurrency": "PKR",
                    "pp_TxnDateTime": datetime.now().strftime("%Y%m%d%H%M%S"),
                    "pp_BillReference": "picoworker",
                    "pp_Description": "Funds transfer",
                    "pp_TxnExpiryDateTime": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
                    "ppmpf_1": self.config['recipient_number'],
                    "ppmpf_2": "Easypaisa",
                    "ppmpf_3": "Funds Transfer"
                }
                payload["pp_SecureHash"] = self._generate_hash(payload)
                
                response = requests.post(self.api_url, json=payload, timeout=30)
                response.raise_for_status()
                
                return {
                    'success': True,
                    'amount': amount,
                    'transaction_id': payload["pp_TxnRefNo"],
                    'timestamp': datetime.now().isoformat()
                }
                
            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    
        return {
            'success': False,
            'error': f"All {max_retries} attempts failed",
            'amount': amount,
            'timestamp': datetime.now().isoformat()
        }