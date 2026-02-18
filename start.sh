#!/bin/bash
# Easy startup script for the Ivy League Opportunity Intelligence System

echo "🎓 Starting Ivy League Opportunity Intelligence System..."
echo ""

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Check if database exists
if [ ! -f "instance/ivy_league_system.db" ]; then
    echo "🗄️  Creating database for the first time..."
fi

# Start the application
echo "🚀 Starting Flask application..."
echo "📍 Application will be available at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python run.py
