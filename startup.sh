#!/bin/bash

# Azure Web App startup script for spaCy model installation
echo "Starting Azure Web App with spaCy model installation..."

# Install spaCy English model if not already installed
python -m spacy download en_core_web_sm --quiet

# Start the Flask application
echo "Starting Flask application..."
gunicorn --bind=0.0.0.0 --timeout 600 app:app
