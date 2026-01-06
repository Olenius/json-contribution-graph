#!/bin/bash

# Quick start script for JSON Contribution Graph Generator

echo "🚀 JSON Contribution Graph Generator"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your settings."
fi

# Generate HTML
echo ""
echo "🎨 Generating HTML..."
python3 generate.py

echo ""
echo "✅ Done! Open index.html in your browser."
echo "💡 To regenerate, run: source venv/bin/activate && python3 generate.py"
