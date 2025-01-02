#!/bin/bash

echo "Starting chatbot launch process..."

# Change to the script's directory
cd "$(dirname "$0")"
echo "Changed to directory: $(pwd)"

# Kill any existing processes on port 8000
echo "Checking for existing processes on port 8000..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Set environment variables
export FLASK_ENV=development
export FLASK_DEBUG=1
export PORT=8000
export MISTRAL_API_URL=http://162.243.42.76
export MISTRAL_API_KEY="L2Nisrbtg4s+KBTgK5fgKRDW+bcI/lx4a8QZ7Odyv7PCO2LWA"

# Verify Python environment
echo "Python version and location:"
which python
python --version

# Install dependencies if needed
if [ ! -f ".deps_installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch .deps_installed
fi

# Start the Flask server in development mode
echo "Starting Flask server..."
python app.py

# Keep the terminal window open
wait