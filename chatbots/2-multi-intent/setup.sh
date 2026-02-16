#!/bin/bash
# Setup script for Multi-Intent Chatbot

echo "Setting up Multi-Intent Chatbot..."

# Create virtual environment
python3 -m venv venv
echo "✅ Virtual environment created"

# Activate virtual environment
source venv/bin/activate
echo "✅ Virtual environment activated"

# Upgrade pip
pip install --upgrade pip > /dev/null 2>&1
echo "✅ pip upgraded"

# Install dependencies
pip install -r requirements.txt > /dev/null 2>&1
echo "✅ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    cat > .env << EOF
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
LOG_LEVEL=INFO
EOF
    echo "✅ .env file created (update with your AWS credentials)"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your AWS credentials"
echo "2. Activate venv: source venv/bin/activate"
echo "3. Run tests: python -m pytest test_chatbot.py -v"
echo "4. Run app: python app.py"
