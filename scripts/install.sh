#!/bin/bash
# Installation script for AI Resepsjonist project

# Create a Python virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Display completion message
echo "Installation complete. Activate the virtual environment with 'source .venv/bin/activate'."
