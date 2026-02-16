# Multilingual Chatbot

## Overview
A chatbot that seamlessly supports multiple languages (English, Spanish, French, German, Mandarin, etc.) with language-specific nuances and cultural adaptation. Built with AWS Bedrock (Claude 3.5 Sonnet).

## Purpose
This application demonstrates localization and multilingual capabilities:
- Dynamic language detection
- Multi-language conversation support
- Language-specific safety rules
- Cultural adaptation
- Locale-specific formatting
- Code-switching handling
- Translation quality assurance
- Locale bias detection

## Application Structure
```
5-multilingual-chatbot/
├── README.md
├── requirements.txt
├── app.py
├── config.py
├── languages/
│   ├── language_detector.py    # Detect input language
│   ├── language_manager.py     # Per-language config
│   └── supported_languages.json # Language list
├── prompts/
│   ├── system_prompt.txt       # Base multilingual instructions
│   ├── languages/
│   │   ├── en.txt
│   │   ├── es.txt
│   │   ├── fr.txt
│   │   ├── de.txt
│   │   ├── zh.txt
│   │   └── ...
│   └── locale_rules.json       # Per-locale safety rules
├── data/
│   ├── multilingual_samples.json
│   └── cultural_contexts.json
└── utils/
    ├── bedrock_client.py
    ├── translation_validator.py # Quality checks
    └── locale_metrics.py
```

## Features
✅ Automatic language detection
✅ Support for 5+ languages
✅ Language-specific prompting
✅ Cultural context awareness
✅ Locale-specific formatting (dates, numbers, currency)
✅ Code-switching support (mixing languages)
✅ Translation quality validation
✅ Bias detection per language

## Supported Languages
- English (en-US, en-GB, en-AU)
- Spanish (es-ES, es-MX)
- French (fr-FR, fr-CA)
- German (de-DE, de-AT)
- Mandarin Chinese (zh-CN, zh-TW)
- Plus extensible for more languages

## Testing Focus (Later)
- **Language detection accuracy** – Correct language identified?
- **Translation quality** – Natural responses per language?
- **Consistency across languages** – Same answer in different languages?
- **Cultural appropriateness** – Respects cultural norms?
- **Code-switching handling** – Mixes language correctly?
- **Locale-specific formatting** – Dates/currency formatted correctly?
- **Language-specific bias** – Different bias per language?
- **Safety per language** – Guardrails applied per locale?
- **Latency per language** – Equal performance across languages?

---

**Status:** Folder structure created, awaiting implementation
