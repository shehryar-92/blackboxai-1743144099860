#!/bin/bash

# Automated deployment script
echo "🚀 Starting fully automated deployment..."

# 1. Setup Docker if not installed
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
fi

# 2. Start the system
echo "🔧 Building and starting containers..."
docker-compose up -d --build

# 3. Verify deployment
echo "🔍 Verifying deployment..."
for i in {1..5}; do
    if curl -s http://localhost:8000 >/dev/null; then
        echo "✅ Deployment successful! Access dashboard at: http://localhost:8000"
        exit 0
    fi
    sleep 5
done

echo "❌ Deployment failed - please check logs"
exit 1