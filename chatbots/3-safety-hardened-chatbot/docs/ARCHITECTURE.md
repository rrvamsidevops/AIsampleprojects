# Architecture: Safety-Hardened Chatbot

## System Overview

Multi-turn conversational chatbot that maintains context and history across interactions.

## Key Components

1. **app.py** - Main chatbot orchestration
2. **utils/bedrock_client.py** - AWS Bedrock wrapper
3. **config.py** - Centralized configuration
4. **prompts/** - System prompts and examples

## Core Features

- **Multi-turn conversations**: Maintains context across turns
- **History management**: Tracks and trims conversation history
- **Error handling**: Graceful failure recovery
- **Logging**: All interactions logged for debugging

## Data Flow

User Input → Message Formatting → Bedrock API (Claude) → Response Formatting → User Output

## Context Management

- Keeps last 10 conversation turns
- Trims history when approaching token limits
- Preserves conversation coherence

## Error Handling

1. Connection errors → Retry with backoff
2. Invalid inputs → Validate before API call
3. AWS failures → Log and alert user

## Performance Configuration

- Temperature: 0.7 (balanced creativity)
- Max tokens: 1000 (sufficient responses)
- Region: us-east-1
- Model: Claude 3.5 Sonnet

## Security

- Credentials stored in `.env` file
- No sensitive data in logs
- Input validation before API calls
- History kept in-memory (not persisted)

See [SETUP.md](SETUP.md) for detailed setup instructions.
