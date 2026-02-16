# Documentation Index

## Quick Navigation

### Getting Started
1. **[AWS Setup](AWS_SETUP.md)** - Configure AWS Bedrock access & IAM permissions
2. **[Testing Guide](TESTING.md)** - Run tests and validate setup

### Key Files Explained

#### In Root Directory
- `app.py` - Main chatbot application
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies
- `setup.sh` / `setup.bat` - Automated environment setup

#### In `prompts/`
- `system_prompt.txt` - Bot personality & instructions
- `examples.json` - Few-shot learning examples

#### In `utils/`
- `bedrock_client.py` - AWS Bedrock integration

#### In `data/`
- `sample_interactions.json` - Test scenarios

#### In `logs/`
- `chatbot.log` - Application logs

---

## Common Tasks

### I want to...

**Run the chatbot**
```bash
source venv/bin/activate
python app.py
```

**Fix AWS permissions**
→ See [AWS Setup](AWS_SETUP.md)

**Run tests**
```bash
# Unit tests (no AWS needed)
python test_chatbot.py

# Integration tests (tests Bedrock API)
python test_integration.py
```

**Update dependencies**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Save a conversation**
In the chatbot, type: `save`

**Reset conversation**
In the chatbot, type: `reset`

---

## Architecture Overview

```
User Input
    ↓
app.py (Main loop)
    ↓
CustomerSupportChatbot class
    ├─ Manages conversation history
    ├─ Formats messages
    └─ Calls Bedrock
    ↓
utils/bedrock_client.py
    ├─ Creates boto3 client
    ├─ Invokes Claude model
    └─ Handles errors
    ↓
AWS Bedrock (Claude 3.5 Sonnet)
    ↓
Response to User
```

---

## Features

✅ **Multi-turn conversations** - Context maintained across turns
✅ **Conversation history** - Full memory of interactions
✅ **Error handling** - Graceful recovery from API failures
✅ **Logging** - All interactions tracked
✅ **Few-shot learning** - Examples improve response quality
✅ **Configuration** - Easy to customize

---

## Troubleshooting

### Error: "bedrock:InvokeModel not authorized"
→ See [AWS Setup - Permissions](AWS_SETUP.md#solution)

### Error: "Unknown service: bedrock-runtime"
→ boto3 version too old. Run: `pip install --upgrade boto3`

### Error: "Empty response from Bedrock"
→ Check AWS credentials: `aws sts get-caller-identity`

### Tests pass but app fails
→ See [Testing Guide - Integration Tests](TESTING.md#2-integration-tests-aws-required)

---

## Next Steps

- Customize system prompt in `prompts/system_prompt.txt`
- Add more few-shot examples in `prompts/examples.json`
- Extend conversation history limit in `config.py`
- Add database persistence for conversations
- Create evaluation framework for testing

---

**Questions?** Check the README.md for overview or specific documentation files above.
