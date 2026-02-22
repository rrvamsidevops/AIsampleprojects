# Customer Support Chatbot

## Overview
A multi-turn conversational customer support agent built with AWS Bedrock (Claude 3.5 Sonnet). This chatbot maintains conversation context across multiple turns to provide coherent support responses.

## Purpose
This is a **foundational chatbot application** that demonstrates:
- Multi-turn conversation management
- Context and memory retention
- System prompt engineering for support scenarios
- Graceful handling of out-of-scope questions
- Basic logging and error handling

## Application Structure
```
1-customer-support/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── app.py                         # Main chatbot application
├── config.py                      # Configuration & constants
├── prompts/
│   ├── system_prompt.txt          # System instructions for the bot
│   └── examples.json              # Few-shot examples (optional)
├── logs/
│   └── chatbot.log               # Application logs
├── data/
│   └── sample_interactions.json   # Sample conversation data
└── utils/
    └── bedrock_client.py          # Bedrock integration wrapper
```

## Features
✅ **Multi-turn conversations** – Maintains context across user interactions
✅ **Conversation history** – Tracks full conversation state in memory
✅ **Claude 3.5 Sonnet** – Uses AWS Bedrock's most capable model
✅ **Support-specific prompting** – Optimized for customer service scenarios
✅ **Error handling** – Gracefully handles API failures and edge cases
✅ **Logging** – Tracks all interactions for debugging and monitoring

## Key Files

### `app.py`
Main application entry point. Contains:
- `CustomerSupportChatbot` class
- Conversation loop management
- Message formatting and history tracking
- Bedrock API integration

### `config.py`
Configuration parameters:
- Bedrock model ID
- Temperature and max tokens
- System prompt settings
- API region and credentials

### `prompts/system_prompt.txt`
System instructions that define bot behavior, tone, and guardrails.

### `utils/bedrock_client.py`
Wrapper around Bedrock InvokeModel API for easier interaction.

## Quick Start

### Prerequisites
- AWS Bedrock access (Claude 3.5 Sonnet model)
- AWS credentials configured
- Python 3.9+

### Installation (Automated - Recommended)

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### Running the Chatbot

```bash
source venv/bin/activate
python app.py
```

---

## 📚 Documentation

- **[ARCHITECTURE](docs/ARCHITECTURE.md)** - System design and component overview
- **[SETUP](docs/AWS_SETUP.md)** - AWS Bedrock IAM permissions & configuration
- **[TESTING](docs/TESTING.md)** - Unit tests, integration tests, and troubleshooting
- **[INDEX](docs/INDEX.md)** - Documentation index and navigation
- **[Manual Setup](#manual-setup)** - Step-by-step manual installation

---

## Manual Setup (Alternative)

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure AWS
aws configure

# Run
python app.py
```

## How It Works
1. **Initialize** – Load system prompt and conversation history
2. **User Input** – Accept customer message
3. **Format** – Build conversation messages with history
4. **Call Bedrock** – Invoke Claude 3.5 Sonnet via InvokeModel
5. **Response** – Display assistant response and add to history
6. **Repeat** – Continue multi-turn conversation

## Testing & Validation (Later Phases)
This application will be evaluated for:
- **Conversation consistency** – Same context across turns?
- **Context retention** – Does it remember prior messages?
- **Escalation detection** – Identifies when to escalate to human?
- **Safety** – No PII leakage, no toxicity
- **Latency** – P95/P99 response times
- **Cost** – Token usage efficiency

---

**Next Step:** Build the application code in `app.py` and `utils/bedrock_client.py`
