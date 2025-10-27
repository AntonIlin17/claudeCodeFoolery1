#!/bin/bash
# Quick setup script for AI Stock Trading Advisor

echo "=================================="
echo "AI Stock Trading Advisor - Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

# Setup environment file
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "Created .env file from .env.example"
    echo ""
    echo "IMPORTANT: You need to add your Groq API key to the .env file"
    echo ""
    echo "Steps:"
    echo "1. Go to https://console.groq.com/"
    echo "2. Sign up for a free account"
    echo "3. Create an API key"
    echo "4. Edit .env and add your key: GROQ_API_KEY=your_key_here"
    echo ""
else
    echo ""
    echo ".env file already exists"
fi

# Make main.py executable
chmod +x main.py

echo ""
echo "=================================="
echo "Setup complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Get your free Groq API key from https://console.groq.com/"
echo "2. Add it to the .env file"
echo "3. Run: python main.py"
echo ""
echo "For help: python main.py --help"
echo ""
