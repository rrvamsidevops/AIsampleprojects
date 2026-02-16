# Conversational Memory Chatbot

## Overview
A stateful chatbot that maintains user profiles, remembers conversation history, and provides personalized responses based on prior interactions. Built with AWS Bedrock (Claude 3.5 Sonnet).

## Purpose
This application demonstrates state management and context persistence:
- User profile maintenance
- Conversation history tracking
- Personality/preference preservation
- Memory retrieval and relevance
- Memory contamination prevention
- Context window management
- Session persistence

## Application Structure
```
4-conversational-memory-chatbot/
├── README.md
├── requirements.txt
├── app.py
├── config.py
├── memory/
│   ├── memory_manager.py       # Memory store & retrieval
│   ├── user_profile.py         # User profile tracking
│   ├── conversation_history.py # Conversation storage
│   ├── memory_cache.py         # In-memory cache
│   └── persistence.py          # Database persistence
├── prompts/
│   ├── system_prompt.txt       # Memory-aware instructions
│   ├── memory_retrieval.txt    # How to use memory context
│   └── examples.json
├── data/
│   ├── user_profiles.json      # Sample user data
│   └── conversation_samples.json
└── utils/
    ├── bedrock_client.py
    └── memory_metrics.py       # Memory quality metrics
```

## Features
✅ User profile creation and updates
✅ Conversation history tracking
✅ Memory retrieval and relevance scoring
✅ Personality consistency across sessions
✅ Context window optimization
✅ Session persistence
✅ Memory summarization for long conversations
✅ Multi-user isolation

## Memory Types

### 1. **Short-term Memory**
- Current conversation context
- Immediate interaction history
- Topic consistency

### 2. **Long-term Memory**
- User preferences
- Personal information
- Past interactions summary
- Known preferences/dislikes

### 3. **Working Memory**
- Currently relevant facts
- Active conversation thread
- Dynamic context updates

## Testing Focus (Later)
- **Memory accuracy** – Does bot remember facts correctly?
- **Context consistency** – Same user = consistent responses?
- **Memory contamination** – Does user A's data leak to user B?
- **Fact hallucination** – Invents false memories?
- **Memory forgetting** – Loses important context?
- **Preference preservation** – Remembers user preferences?
- **Session isolation** – Different users kept separate?
- **Performance with history** – Does long history slow responses?

---

**Status:** Folder structure created, awaiting implementation
