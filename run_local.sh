#!/bin/bash

# Kill any existing Python processes
pkill -f python3
pkill -f gunicorn

# Set environment variables
export FLASK_ENV=development
export PORT=8000
export MISTRAL_API_URL=https://api.mistral.ai/v1
export MISTRAL_API_KEY=your_key_here  # Replace with your actual key

# Run the app using Flask for development
python3 app.py