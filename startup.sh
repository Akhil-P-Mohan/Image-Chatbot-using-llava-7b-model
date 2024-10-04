#!/bin/bash

# Set the working directory to the root of the repository
cd /home/site/wwwroot

# Activate the virtual environment
source venv/bin/activate

# Run the Flask app
gunicorn -w 4 -b 0.0.0.0:8080 app:app
