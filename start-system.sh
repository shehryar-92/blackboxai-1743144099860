#!/bin/bash

# Initialize system and send test email
echo "🚀 Starting Picoworker Automation System..."

# 1. Set up permissions
chmod +x auto-deploy.sh setup-crontab.sh monitoring/healthcheck.sh

# 2. Configure automatic updates
./setup-crontab.sh

# 3. Start health monitoring
nohup ./monitoring/healthcheck.sh > /var/log/picoworker-monitor.log 2>&1 &

# 4. Deploy the application
./auto-deploy.sh

# 5. Send immediate test email
echo "Sending verification email to shehryarzahid94@gmail.com..."
echo "Subject: Picoworker System Started Successfully

Your Picoworker automation system is now active and monitoring payments.

System Details:
- Startup Time: $(date)
- Dashboard URL: http://localhost:8000
- Next $5 payment will trigger confirmation email

You don't need to do anything - the system will run automatically." | sendmail shehryarzahid94@gmail.com

echo "✅ System started successfully - check your email for verification"