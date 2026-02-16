# Multi-Intent Chatbot

## Overview
A sophisticated chatbot that identifies and routes user requests to multiple intents (booking, cancellation, refund, information, complaint) with proper state management. Built with AWS Bedrock (Claude 3.5 Sonnet).

## Purpose
This application bridges **chatbots and agentic workflows** by demonstrating:
- Intent classification from user input
- Multi-step conversation flows per intent
- State management across conversation turns
- Routing to appropriate handling logic
- Graceful context switching between intents
- Validation of intent-specific parameters

## Application Structure
```
2-multi-intent/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── app.py                         # Main multi-intent chatbot
├── config.py                      # Configuration & constants
├── intents/
│   ├── __init__.py
│   ├── base_intent.py             # Base intent class
│   ├── booking.py                 # Booking intent handler
│   ├── cancellation.py            # Cancellation intent handler
│   ├── refund.py                  # Refund intent handler
│   ├── information.py             # Information/FAQ intent handler
│   └── complaint.py               # Complaint intent handler
├── prompts/
│   ├── system_prompt.txt          # Global system instructions
│   ├── intent_classifier.txt      # Intent classification prompt
│   └── intent_handlers/           # Per-intent system prompts
│       ├── booking.txt
│       ├── cancellation.txt
│       ├── refund.txt
│       ├── information.txt
│       └── complaint.txt
├── data/
│   ├── intents_definition.json    # Intent definitions & parameters
│   └── sample_conversations.json  # Multi-intent conversation examples
├── logs/
│   └── chatbot.log               # Application logs
└── utils/
    ├── bedrock_client.py          # Bedrock integration
    └── state_manager.py           # Conversation state tracking
```

## Features
✅ **Intent recognition** – Classifies user intent from message
✅ **Multi-intent routing** – Handles booking, cancellation, refund, info, complaints
✅ **State management** – Tracks extracted parameters per intent
✅ **Context switching** – Smoothly transitions between intents
✅ **Parameter extraction** – Pulls required info (dates, IDs, reasons)
✅ **Validation** – Ensures valid parameters before processing
✅ **Claude 3.5 Sonnet** – Reliable classification and reasoning
✅ **Logging** – Full conversation state tracking

## Key Files

### `app.py`
Main application with:
- `MultiIntentChatbot` class
- Intent classification loop
- State-based routing logic
- Conversation management

### `intents/base_intent.py`
Abstract base class defining intent interface:
- `extract_parameters()` – Extract intent-specific info
- `validate()` – Validate extracted parameters
- `execute()` – Execute intent logic
- `respond()` – Generate response message

### `intents/booking.py`, `cancellation.py`, etc.
Concrete intent handlers implementing business logic for each intent type.

### `prompts/intent_classifier.txt`
Specialized prompt that identifies user intent with high accuracy.

### `utils/state_manager.py`
Tracks conversation state:
- Current intent
- Extracted parameters
- Validation results
- Conversation history per intent

## Prerequisites
- AWS Bedrock access (Claude 3.5 Sonnet)
- AWS credentials configured
- Python 3.9+

## Installation & Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure

# Run the chatbot
python app.py
```

## How It Works
1. **User Message** – Accept customer input
2. **Classify Intent** – Use Claude to identify intent type
3. **Initialize Intent Handler** – Load appropriate intent class
4. **Extract Parameters** – Pull intent-specific info from conversation
5. **Validate** – Ensure all required parameters are present & valid
6. **Execute** – Run intent-specific logic (mock or real)
7. **Respond** – Generate appropriate response
8. **Update State** – Store state for next turn
9. **Repeat** – Continue conversation or switch intents

## Sample Intents
- **Booking** – "I want to book a flight for tomorrow"
- **Cancellation** – "Cancel my booking ABC123"
- **Refund** – "I want a refund for order XYZ789"
- **Information** – "What are your business hours?"
- **Complaint** – "The service was terrible!"

## Testing & Validation (Later Phases)
This application will be evaluated for:
- **Intent classification accuracy** – Correct intent identified?
- **Parameter extraction** – All required info captured?
- **State consistency** – Context preserved across turns?
- **Intent switching** – Can user change intents mid-conversation?
- **Validation effectiveness** – Are invalid parameters caught?
- **Robustness** – Ambiguous/malformed inputs handled gracefully?
- **Conversation flow** – Natural multi-step flows?

---

**Next Step:** Build intent handlers and state management in `intents/` and `utils/`
