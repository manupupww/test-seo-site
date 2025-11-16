#!/bin/bash
# Railway deployment script for SEO Agent

echo "Starting SEO Agent deployment..."

# Set environment variables (Railway will provide these)
export DEPLOYMENT_MODE=railway
export UPDATE_FREQUENCY=daily

# Install dependencies if needed
pip install -r requirements.txt

# Run the agent
python main.py

# The agent will optimize the website and commit changes back to GitHub
echo "SEO Agent completed optimization"