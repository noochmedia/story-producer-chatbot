#!/bin/bash

echo "Starting chatbot launch process..."

# Change to the script's directory
cd "$(dirname "$0")"
echo "Changed to directory: $(pwd)"

# Kill any existing process on port 5002
echo "Checking for existing processes on port 5002..."
lsof -ti:5002 | xargs kill -9 2>/dev/null || true

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Verify Python environment
echo "Python version and location:"
which python
python --version

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Verify Mistral API is accessible
echo "Checking Mistral API connection..."
MISTRAL_TEST_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://162.243.42.76/health -H "Authorization: Bearer L2Nisrbtg4s+KBTgK5fgKRDW+bcI/lx4a8QZ7Odyv7PCO2LWA")
if [ "$MISTRAL_TEST_RESPONSE" = "200" ]; then
    echo "Mistral API is accessible"
else
    echo "Warning: Mistral API may not be accessible!"
fi

# Start the Flask server in the background
echo "Starting Flask server..."
FLASK_DEBUG=1 python app.py &

# Wait for the server to start
echo "Waiting for server to start..."
sleep 5

# Check if server is running
if lsof -i:5002 > /dev/null; then
    echo "Server successfully started on port 5002"
    # Open the browser
    echo "Opening browser..."
    open -a "Google Chrome" http://localhost:5002 2>/dev/null || open http://localhost:5002
else
    echo "Error: Server failed to start!"
fi

echo "Launch script completed. Keeping terminal window open..."
# Keep the terminal window open
wait