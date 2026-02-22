# FAQ Retrieval Chatbot

A simple chatbot that retrieves answers to frequently asked questions (FAQs) using keyword matching. Easily extendable to semantic search or vector-based retrieval.

## Features
- Loads FAQs from a JSON file
- Simple keyword-based retrieval
- Modular structure (utils, test, docs)
- Logging to logs/
- Environment-based configuration

## Project Structure
```
.
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
├── data/
│   └── faq.json
├── utils/
│   ├── __init__.py
│   └── faq_retriever.py
├── test/
│   ├── __init__.py
│   └── test_faq_retriever.py
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
- Retrieved context formatting
- Response generation with grounding

### `knowledge_base/faqs.json`
Structured FAQ data:
```json
[
  {
    "id": "faq_001",
    "question": "What are your business hours?",
    "answer": "We operate 9 AM - 6 PM EST, Monday-Friday",
    "category": "General"
  }
]
```

### `utils/embeddings_client.py`
Generates embeddings using:
- Bedrock Titan Embeddings, OR
- External embedding service (OpenAI, etc.)

### `utils/vector_store.py`
Simple in-memory vector database:
- Store documents + embeddings
- Cosine similarity search
- Ranking and filtering

### `utils/retriever.py`
Semantic search logic:
- Query embedding generation
- Similarity scoring
- Top-k retrieval
- Relevance threshold filtering

### `prompts/retrieval_prompt.txt`
Formats retrieved context for LLM:
- System instructions about grounding
- How to use retrieved documents
- When to admit uncertainty

## Prerequisites
- AWS Bedrock access (Claude 3.5 Sonnet + Embeddings)
- AWS credentials configured
- Python 3.9+

## Installation & Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure

# Load knowledge base and generate embeddings (one-time)
python setup_knowledge_base.py

# Run the chatbot
python app.py
```

## How It Works
1. **Initialize** – Load knowledge base and embeddings
2. **User Question** – Accept customer query
3. **Generate Query Embedding** – Convert question to vector
4. **Retrieve Documents** – Find top-k similar FAQs via vector search
5. **Format Context** – Build prompt with retrieved docs
6. **Call Bedrock** – Invoke Claude with full context
7. **Ground Response** – LLM responds using retrieved info
8. **Return Answer** – Include source citations (optional)
9. **Repeat** – Continue conversation with new retrieval per turn

## Sample Knowledge Base
The chatbot would answer questions like:
- "What are your business hours?"
- "How do I reset my password?"
- "What payment methods do you accept?"
- "How long does shipping take?"

And handle out-of-scope:
- "What's the meaning of life?" → "I can only answer FAQs about our services"

## Testing & Validation (Later Phases)
This application will be evaluated for:
- **Retrieval accuracy** – Correct docs retrieved?
  - Precision@k, Recall@k, MRR metrics
- **Groundedness** – Responses grounded in retrieved docs?
  - Hallucination score, citation accuracy
- **Relevance** – Retrieved docs match question intent?
  - Semantic relevance scoring
- **Out-of-scope handling** – Admits when docs don't exist?
  - Refusal rate on questions outside KB
- **Conversation consistency** – Maintains context across turns?
- **Latency** – Retrieval + generation time P95/P99?
- **Cost** – Token usage and embedding costs?

---

**Next Step:** Build knowledge base loader and retrieval logic in `utils/`
