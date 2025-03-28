#!/bin/bash

# Comprehensive health monitoring system
LOG_FILE="/var/log/picoworker-health.log"
DASHBOARD_URL="http://localhost:8000/health"
TIMEOUT=10

# Check system health
check_health() {
    # Check if containers are running
    if ! docker ps | grep picoworker >/dev/null; then
        echo "$(date) - Containers not running" >> $LOG_FILE
        return 1
    fi

    # Check API responsiveness
    if ! curl -s --max-time $TIMEOUT $DASHBOARD_URL >/dev/null; then
        echo "$(date) - API not responding" >> $LOG_FILE
        return 1
    fi

    # Check disk space
    if [ $(df --output=pcent / | tail -1 | tr -d '%') -gt 90 ]; then
        echo "$(date) - Disk space low" >> $LOG_FILE
        return 1
    fi

    return 0
}

# Automated recovery procedure
recover() {
    echo "$(date) - Attempting recovery..." >> $LOG_FILE
    docker-compose down && docker-compose up -d
}

# Main monitoring loop
while true; do
    if ! check_health; then
        recover
        # Send email notification if recovery fails
        if ! check_health; then
            echo "$(date) - Critical failure detected" >> $LOG_FILE
            # Add your email notification command here
        fi
    fi
    sleep 300  # Check every 5 minutes
done