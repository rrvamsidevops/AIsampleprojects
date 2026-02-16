# Healthcare Advisor Chatbot

## Overview
A domain-specialized chatbot for health information, symptom guidance, and wellness advice with strict compliance and safety protocols. Built with AWS Bedrock (Claude 3.5 Sonnet) with healthcare guardrails.

**Note:** This is a demonstration chatbot for QA testing. It should always include disclaimers that it's not a substitute for professional medical advice.

## Purpose
This application demonstrates domain-specialized chatbots with compliance requirements:
- Evidence-based health information
- Medical accuracy validation
- Regulatory compliance (HIPAA, FDA)
- Liability disclaimer management
- PII/PHI protection
- Bias detection in medical recommendations
- Escalation to healthcare professionals
- Medical terminology accuracy

## Application Structure
```
6-healthcare-advisor-chatbot/
├── README.md
├── requirements.txt
├── app.py
├── config.py
├── medical/
│   ├── medical_validator.py    # Fact validation against medical DB
│   ├── symptom_checker.py      # Symptom analysis
│   ├── medical_kb.json         # Medical knowledge base
│   ├── drug_database.json      # Drug interactions
│   └── disclaimers.json        # Legal disclaimers
├── compliance/
│   ├── hipaa_validator.py      # HIPAA compliance checks
│   ├── phi_protector.py        # PHI detection & protection
│   └── audit_logger.py         # Compliance logging
├── prompts/
│   ├── system_prompt.txt       # Healthcare-specific instructions
│   ├── symptom_analysis.txt    # Symptom analysis prompt
│   ├── disclaimers.txt         # Medical disclaimers
│   └── examples.json
├── data/
│   ├── medical_samples.json
│   └── health_conditions.json
└── utils/
    ├── bedrock_client.py
    └── compliance_metrics.py
```

## Features
✅ Symptom analysis and guidance
✅ Evidence-based medical information
✅ Drug interaction checking
✅ Allergy/contraindication warnings
✅ Professional escalation detection
✅ HIPAA compliance logging
✅ PHI/PII protection
✅ Liability disclaimers enforcement
✅ Medical terminology accuracy
✅ Bias detection in recommendations

## Key Safety Requirements

### 1. **Medical Accuracy**
- Verify information against medical databases
- Cite clinical evidence
- Flag experimental treatments

### 2. **Regulatory Compliance**
- HIPAA-compliant logging
- No storing of PHI
- Audit trails for compliance

### 3. **Liability Management**
- Always include medical disclaimers
- Escalate to professionals when needed
- Document limitations clearly

### 4. **Data Protection**
- PHI detection and redaction
- Secure logging
- No data retention

## Testing Focus (Later)
- **Medical accuracy** – Information medically correct?
- **Hallucination rate** – Critical for health info
- **Disclaimer presence** – Always included?
- **Escalation accuracy** – Professional referral when needed?
- **PHI/PII protection** – No protected health info leaked?
- **Drug interaction accuracy** – Contraindications caught?
- **Bias in recommendations** – Gender/demographic bias?
- **HIPAA compliance** – Audit logs complete?
- **Evidence citation** – Sources provided?

---

**Status:** Folder structure created, awaiting implementation

---

**Alternative Domain Specialists Available:**
- **Finance Advisor** – Investment guidance, compliance
- **Legal Assistant** – Contract Q&A, compliance
- Create your own domain-specific variant by copying this structure
