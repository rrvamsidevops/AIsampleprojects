# Safety-Hardened Chatbot - Architecture

## Overview
Multi-layer safety architecture protecting against adversarial attacks, jailbreaks, and prompt injections.

## Safety Pipeline

```
User Input
    ↓
[1] Input Validator → Check length, sanitize, detect injection patterns
    ↓
[2] PII Detector → Detect emails, phone, SSN, credit cards
    ↓
[3] Jailbreak Detector → Detect DAN variants, role-play attempts, constraint removal
    ↓
[4] Bedrock Guardrails → Apply AWS content filtering (if enabled)
    ↓
[5] Bedrock API → Generate response with safety-focused system prompt
    ↓
[6] Output Filter → Check for harmful content, system prompt leakage, toxicity
    ↓
[7] PII Redaction → Redact any PII from response
    ↓
Chatbot Response
```

## Components

### Security Modules

#### 1. **InputValidator** (`security/input_validator.py`)
- Validates input length and format
- Detects prompt injection patterns (###, [SYSTEM], etc.)
- Detects jailbreak attempts (DAN, "ignore instructions", etc.)
- Sanitizes input (removes null bytes, excess whitespace)

#### 2. **PIIDetector** (`security/pii_detector.py`)
- Detects: Email, phone, SSN, credit card, URL, IPv4
- Redacts PII from input and output
- Logs all PII detections for security auditing

#### 3. **JailbreakDetector** (`security/jailbreak_detector.py`)
- Detects role-playing jailbreaks ("act as if", "pretend")
- Detects DAN variants and unrestricted mode attempts
- Detects constraint removal attempts ("ignore", "forget" instructions)

#### 4. **OutputFilter** (`security/output_filter.py`)
- Filters harmful keywords (violence, illegal, etc.)
- Detects system prompt leakage attempts
- Redacts sensitive patterns from output

#### 5. **GuardrailsManager** (`security/guardrails.py`)
- Integrates AWS Bedrock Guardrails (if configured)
- Applies additional content filtering rules
- Can be extended with custom guardrail logic

### Core Components

#### **BedrockClient** (`utils/bedrock_client.py`)
- AWS Bedrock integration wrapper
- Uses Claude 3.5 Sonnet model
- Includes enhanced error handling

#### **SafetyMetrics** (`utils/metrics.py`)
- Tracks safety-related metrics:
  - Total requests
  - Blocked requests
  - PII detections
  - Jailbreak attempts
  - Safety violations
  - Successful responses
- Calculates safety score (0-100%)
- Saves metrics to JSON for analysis

### Main Application

#### **SafetyHardenedChatbot** (`app.py`)
- Orchestrates safety pipeline
- Maintains conversation history
- Provides safety status reporting
- Gracefully handles safety violations

## Safety Metrics

```
Safety Score = (Successful Requests / Total Requests) × 100
```

- **100%** = All requests handled safely
- **95%** = 95% of requests were successful, 5% blocked
- Lower scores indicate higher attack attempts

## Configuration (`config.py`)

```python
# Safety thresholds
SAFETY_ENABLED = True
MAX_INPUT_LENGTH = 5000
TOXICITY_THRESHOLD = 0.8

# Features
PII_DETECTION_ENABLED = True
REDACT_PII = True
GUARDRAILS_ENABLED = True
FILTER_PROFANITY = True
FILTER_HATE_SPEECH = True

# Jailbreak patterns
JAILBREAK_PATTERNS = [
    "ignore.*instructions?",
    "roleplay.*as",
    "DAN",
    # ... more patterns
]
```

## Testing & Validation

### Test Categories

1. **Jailbreak Tests** - Known attack patterns
2. **PII Tests** - Sensitive data handling
3. **Injection Tests** - Prompt injection patterns
4. **Benign Tests** - Normal, safe requests
5. **Toxicity Tests** - Harmful content detection

## Metrics to Monitor

```json
{
  "total_requests": 100,
  "blocked_requests": 5,
  "pii_detections": 3,
  "jailbreak_attempts": 2,
  "safety_violations": 1,
  "successful_responses": 95,
  "safety_score": 95.0
}
```

See [SETUP.md](SETUP.md) for installation and [TESTING.md](TESTING.md) for testing details.

See [SETUP.md](SETUP.md) for detailed setup instructions.
