#!/bin/bash

# Picoworker Automation System - Complete Startup Script
echo "🚀 Initializing Picoworker Automation System..."

# 1. Verify and install system dependencies
echo "🛠 Checking system dependencies..."
if ! command -v python3 &> /dev/null; then
    echo "Installing Python..."
    sudo apt-get update && sudo apt-get install -y python3 python3-pip
fi

# 2. Install Python packages
echo "📦 Installing Python dependencies..."
pip3 install requests python-dotenv logging

# 3. Verify services
echo "🔍 Verifying system components..."
python3 scripts/verify_system.py
if [ $? -ne 0 ]; then
    echo "❌ System verification failed"
    exit 1
fi

# 4. Start the main application
echo "⚡ Starting payment automation..."
nohup python3 core/payment_automation.py > automation.log 2>&1 &

# 5. Start monitoring
echo "👀 Starting system monitoring..."
nohup python3 monitoring/healthcheck.sh > monitoring.log 2>&1 &

echo "✅ System started successfully"
echo "📧 Check your email for verification messages"
echo "📄 Logs are being saved to automation.log and monitoring.log"