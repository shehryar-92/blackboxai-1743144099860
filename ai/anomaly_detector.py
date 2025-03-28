import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime
import json
import os

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.01)
        self.data_file = "ai/transaction_history.json"
        self.load_data()
        
    def load_data(self):
        """Load or initialize transaction history"""
        if os.path.exists(self.data_file):
            with open(self.data_file) as f:
                self.history = json.load(f)
        else:
            self.history = {"amounts": [], "timestamps": []}
            
    def save_data(self):
        """Save transaction history"""
        with open(self.data_file, 'w') as f:
            json.dump(self.history, f)
            
    def add_transaction(self, amount):
        """Record new transaction"""
        self.history["amounts"].append(float(amount))
        self.history["timestamps"].append(datetime.now().isoformat())
        self.save_data()
        
    def detect_anomalies(self):
        """Check for abnormal transactions"""
        if len(self.history["amounts"]) < 10:  # Minimum data points
            return False
            
        amounts = np.array(self.history["amounts"]).reshape(-1, 1)
        self.model.fit(amounts)
        predictions = self.model.predict(amounts[-10:])  # Check last 10
        return any(p == -1 for p in predictions)  # -1 indicates anomaly
        
    def handle_anomaly(self, amount):
        """Take action on detected anomaly"""
        print(f"ANOMALY DETECTED: ${amount}")
        # Add your custom anomaly handling logic here
        return True