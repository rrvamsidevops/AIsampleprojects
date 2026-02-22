
# Conversational Memory Chatbot

> A memory-enabled chatbot template with modular structure, environment-based configuration, and ready for LLM integration. Follows standards from other chatbots in this repository.

## Features
- MemoryManager for short-term and long-term memory
- Modular structure (utils, prompts, test, docs)
- Environment-based configuration via `.env`
- Logging to `logs/`
- Prompt templates and examples
- Ready for LLM integration (AWS Bedrock, OpenAI, etc.)

## Project Structure
```
.
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
├── utils/
│   ├── __init__.py
│   └── memory.py
├── prompts/
│   ├── system_prompt.txt
│   └── examples/
│       └── examples.json
├── data/
│   └── sample_interactions.json
├── test/
│   ├── __init__.py
│   └── test_memory.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── INDEX.md
│   ├── SETUP.md
│   └── TESTING.md
├── logs/
```

## Setup
See [docs/SETUP.md](docs/SETUP.md) for environment and installation instructions.

## Architecture
See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for design and extensibility notes.

## Testing
Run tests with:
```bash
python -m unittest discover -s test
```

## License
MIT
