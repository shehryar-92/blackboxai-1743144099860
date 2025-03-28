import requests
import hashlib
import json
from datetime import datetime

class JazzCashClient:
    def __init__(self):
        self.merchant_id = "YOUR_MERCHANT_ID"
        self.password = "YOUR_API_PASSWORD"
        self.salt = "YOUR_SALT_KEY"
        self.api_url = "https://sandbox.jazzcash.com.pk/ApplicationAPI/API/2.0/Payment/DoTransaction"
        
    def _generate_hash(self, params):
        data = '|'.join(str(v) for v in params.values()) + self.salt
        return hashlib.sha256(data.encode()).hexdigest()

    def transfer_to_easypaisa(self, amount, recipient_number):
        """Transfer funds from JazzCash to Easypaisa"""
        try:
            payload = {
                "pp_Version": "2.0",
                "pp_TxnType": "MWALLET",
                "pp_Language": "EN",
                "pp_MerchantID": self.merchant_id,
                "pp_SubMerchantID": "",
                "pp_Password": self.password,
                "pp_BankID": "",
                "pp_ProductID": "",
                "pp_TxnRefNo": f"TXN{datetime.now().timestamp()}",
                "pp_Amount": str(amount * 100),  # in paisa
                "pp_TxnCurrency": "PKR",
                "pp_TxnDateTime": datetime.now().strftime("%Y%m%d%H%M%S"),
                "pp_BillReference": "picoworker",
                "pp_Description": "Funds transfer",
                "pp_TxnExpiryDateTime": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
                "pp_ReturnURL": "",
                "pp_SecureHash": "",
                "ppmpf_1": recipient_number,  # Easypaisa number
                "ppmpf_2": "Easypaisa",
                "ppmpf_3": "Funds Transfer",
                "ppmpf_4": "",
                "ppmpf_5": ""
            }
            payload["pp_SecureHash"] = self._generate_hash(payload)
            
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            
            return {
                "success": True,
                "transaction_id": response.json().get("pp_TxnRefNo"),
                "response": response.json()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": response.json() if 'response' in locals() else None
            }