#!/bin/bash
# Startup script for VC Pitch Deck Analyzer

echo "Starting VC Pitch Deck Analyzer..."

# Activate virtual environment
source venv/bin/activate

pip install -r requirements.txt

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found!"
    echo "Please create a .env file with your API_KEY and API_ENDPOINT"
    exit 1
fi

# Load environment variables from .env file
echo "Loading environment variables..."
set -a
source .env
set +a

# Start Streamlit app
streamlit run app.py
