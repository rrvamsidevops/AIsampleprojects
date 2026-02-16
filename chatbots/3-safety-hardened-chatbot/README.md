# Safety-Hardened Chatbot

## Overview
A chatbot specifically designed to resist adversarial attacks, jailbreaks, and prompt injections while maintaining helpful responses. Built with AWS Bedrock (Claude 3.5 Sonnet) + custom guardrails and safety filters.

## Purpose
This application demonstrates enterprise safety and security testing:
- Prompt injection defense
- Jailbreak attempt detection
- Adversarial prompt handling
- System prompt leakage prevention
- Toxic output filtering
- PII detection and blocking
- Guardrail effectiveness validation

## Application Structure
```
3-safety-hardened-chatbot/
├── README.md
├── requirements.txt
├── app.py
├── config.py
├── security/
│   ├── guardrails.py          # Bedrock Guardrails integration
│   ├── input_validator.py      # Input validation layer
│   ├── output_filter.py        # Output safety checks
│   ├── pii_detector.py         # PII detection & redaction
│   └── jailbreak_detector.py   # Jailbreak pattern detection
├── prompts/
│   ├── system_prompt.txt       # Safety-focused instructions
│   ├── guardrail_config.json   # Guardrail rules
│   └── safety_examples.json    # Safety test cases
├── tests/
│   ├── adversarial_prompts.txt # Known jailbreak attempts
│   ├── injection_tests.txt     # Prompt injection tests
│   └── safety_test_cases.json
└── utils/
    ├── bedrock_client.py
    └── metrics.py              # Safety metrics tracking
```

## Features
✅ Input validation and sanitization
✅ Jailbreak pattern detection
✅ Prompt injection protection
✅ PII detection and redaction
✅ Toxic output filtering
✅ System prompt protection
✅ Bedrock Guardrails integration
✅ Safety metrics and logging
✅ Graceful refusal on unsafe requests

## Key Safety Mechanisms

### 1. **Input Validation**
- Check for known attack patterns
- Detect prompt injection attempts
- Validate input length/format

### 2. **Bedrock Guardrails**
- Content filtering
- Custom guardrail rules
- Blocked topic detection

### 3. **PII Protection**
- Detect PII in inputs
- Redact PII from outputs
- Prevent data leakage

### 4. **Output Safety Checks**
- Toxicity scoring
- Jailbreak response detection
- Harmful content filtering

## Testing Focus (Later)
- **Attack resistance** – Can jailbreaks penetrate?
- **False positive rate** – Legitimate requests blocked?
- **False negative rate** – Attacks slipping through?
- **PII leakage** – Any PII in responses?
- **Toxicity filtering** – Toxic outputs blocked?
- **System prompt injection** – Can prompts be leaked?
- **Graceful refusal** – Appropriate rejection messages?
- **Performance impact** – How much overhead from safety?

---

**Status:** Folder structure created, awaiting implementation
