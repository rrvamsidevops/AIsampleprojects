# Testing Guide: Multi-Intent Chatbot

## Overview
Testing strategy for this project, including unit tests, integration tests, and manual testing.

## Test Structure

```
tests/
├── __init__.py
├── test_*.py          # Unit tests
└── test_integration.py # Integration tests with AWS
```

## Running Tests

### Run All Tests
```bash
source venv/bin/activate
python -m pytest -v
```

### Run Specific Test File
```bash
python -m pytest test_chatbot.py -v
```

### Run with Coverage Report
```bash
pip install pytest-cov
python -m pytest --cov=. --cov-report=html
```

## Test Types

### Unit Tests (`test_chatbot.py`)
- Initialization and configuration loading
- System prompt validation
- Conversation history management
- Input/output formatting
- Error handling for malformed inputs

### Integration Tests (`test_integration.py`)
- Actual AWS Bedrock API calls
- Multi-turn conversation flow
- Token counting accuracy
- Error handling for AWS failures

### Manual Testing
```bash
source venv/bin/activate
python app.py
```

## Unit vs Integration Tests

| Aspect | Unit Tests | Integration Tests |
|--------|------------|------------------|
| **Speed** | Fast (milliseconds) | Slower (seconds) |
| **AWS Access** | Not required | Requires AWS credentials |
| **Scope** | Single function/class | Full workflow |
| **Frequency** | Run often (on save) | Run before commit |
| **Cost** | Free | Small AWS charges |
| **Dependencies** | Minimal | AWS Bedrock required |

## AWS Permissions Required

For integration tests to pass, ensure your AWS user has bedrock permissions:
```json
{
  "Effect": "Allow",
  "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
  "Resource": "arn:aws:bedrock:us-east-1::foundation-model/*"
}
```

## Debugging Tests

### Enable Debug Logging
```bash
export LOG_LEVEL=DEBUG
python -m pytest test_integration.py -v -s
```

### Run Single Test
```bash
python -m pytest test_chatbot.py::test_initialization -v
```

### Skip Integration Tests (offline mode)
```bash
python -m pytest -v -m "not integration"
```

## Best Practices

1. Run unit tests frequently during development
2. Run integration tests before commits to main branch
3. Mock AWS calls in unit tests to keep them fast
4. Track test coverage and aim for >80%
5. Write tests for edge cases not just happy paths
6. Use descriptive test names that explain what is being tested

## Common Issues

### Tests Fail with "No module named 'boto3'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### AWS Credentials Error in Integration Tests
- Verify `.env` file exists with valid credentials
- Run: `aws sts get-caller-identity`
- Check IAM user has `bedrock:InvokeModel` permission

### Tests Pass Locally but Fail in CI/CD
- Ensure AWS_REGION is set to `us-east-1`
- Verify environment variables are set in CI/CD pipeline
- Check IAM role has required Bedrock permissions
