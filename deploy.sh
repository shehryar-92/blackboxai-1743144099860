#!/bin/bash

# Set up environment
echo "Setting up the environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install fastapi uvicorn websockets requests scikit-learn

# Start the application
echo "Starting the application..."
uvicorn server.app:app --host 0.0.0.0 --port 8000 --reload