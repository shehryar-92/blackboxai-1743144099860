import requests
from decimal import Decimal
import time
from datetime import datetime

class EasypaisaClient:
    def __init__(self, account_number):
        self.account = account_number
        self.base_url = "https://easypaisa.com.pk/api/v1"
        self.session = requests.Session()
        self.last_request = None
        
    def _make_request(self, endpoint, params=None):
        """Handle rate limiting and retries"""
        if self.last_request and (time.time() - self.last_request) < 1:
            time.sleep(1)  # Respect rate limits
            
        try:
            response = self.session.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                headers={"Authorization": "Bearer YOUR_API_KEY"},
                timeout=10
            )
            self.last_request = time.time()
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[{datetime.now()}] API Error: {str(e)}")
            raise

    def check_balance(self):
        """Get current account balance"""
        data = self._make_request(f"accounts/{self.account}/balance")
        return Decimal(data['available_balance'])

    def get_recent_transactions(self, hours=24):
        """Retrieve transactions from last N hours"""
        params = {"hours": hours}
        data = self._make_request(f"accounts/{self.account}/transactions", params)
        return data['transactions']

    def verify_payment(self, amount):
        """Check if specific amount was received"""
        transactions = self.get_recent_transactions()
        return any(
            Decimal(t['amount']) == Decimal(amount) 
            and t['status'] == 'completed'
            for t in transactions
        )