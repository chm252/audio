#!/bin/bash

# Exit on error
set -e

echo "Starting..."

# Check if Python and Node.js are installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed."
    exit 1
fi

if ! command -v npm &> /dev/null
then
    echo "Node.js is not installed."
    exit 1
fi

echo "Installing axios..."
npm install axios
npm install axios@0.27.2
npm install --save-dev jest @testing-library/react @testing-library/jest-dom

echo "Installing ffmpeg..."
sudo apt-get update && sudo apt-get install -y ffmpeg

# Create and activate a virtual environment for Python
echo "Creating Python virtual environment..."
python3 -m venv backend/venv
source backend/venv/bin/activate

# Install backend dependencies
echo "Installing backend dependencies..."
pip install -r backend/requirements.txt

# Initialize the SQLite database
echo "Initializing SQLite database..."
python3 backend/init_db.py

# Deactivate virtual environment
deactivate

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install --save-dev jest
cd ..

echo "Setup complete!"

