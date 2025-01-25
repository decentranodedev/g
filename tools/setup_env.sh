#!/bin/bash

# Setup script for DecentraNode environment

echo "Setting up the DecentraNode environment..."

# Step 1: Create and activate a Python virtual environment
if [ ! -d "venv" ]; then
    echo "Creating a Python virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

echo "Activating the virtual environment..."
source venv/bin/activate

# Step 2: Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies from requirements.txt..."
    pip install -r requirements.txt
    echo "Python dependencies installed."
else
    echo "requirements.txt not found. Skipping Python dependency installation."
fi

# Step 3: Install Node.js dependencies
if [ -f "package.json" ]; then
    echo "Installing Node.js dependencies from package.json..."
    npm install
    echo "Node.js dependencies installed."
else
    echo "package.json not found. Skipping Node.js dependency installation."
fi

# Step 4: Set up the database
echo "Setting up the database..."
python3 -c "
from src.backend.models import db
from src.backend.app import app
with app.app_context():
    db.create_all()
"
echo "Database setup complete."

# Step 5: Final messages
echo "Environment setup complete. You can now run the platform:"
echo "  - To start the backend: source venv/bin/activate && python src/backend/app.py"
echo "  - To start the frontend: npm start in the frontend folder"

exit 0
