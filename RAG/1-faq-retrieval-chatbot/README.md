# FAQ Retrieval Chatbot (RAG Application)

## Overview
A conversational FAQ chatbot that retrieves relevant answers from a knowledge base and grounds responses in retrieved documents. Built with AWS Bedrock (Claude 3.5 Sonnet) + vector embeddings for semantic search.

## Purpose
This is a **foundational RAG application** that demonstrates:
- Document ingestion and embedding generation
- Vector-based semantic retrieval
- Multi-turn conversation with retrieval context
- Grounding responses in retrieved documents
- Handling out-of-context questions gracefully
- Integration of retrieval with conversational AI

## Application Structure
```
1-faq-retrieval-chatbot/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── app.py                         # Main RAG chatbot application
├── config.py                      # Configuration & constants
├── knowledge_base/
│   ├── faqs.json                 # FAQ documents
│   └── documents.md              # Raw markdown documents
├── embeddings/
│   ├── embeddings.pkl            # Cached embeddings (vector DB)
│   └── embeddings_index.json     # Index mapping
├── prompts/
│   ├── system_prompt.txt         # System instructions for bot
│   ├── retrieval_prompt.txt      # Context formatting prompt
│   └── examples.json             # Few-shot examples
├── logs/
│   └── chatbot.log              # Application logs
├── data/
│   ├── sample_interactions.json  # Sample Q&A interactions
│   └── retrieval_metrics.json    # Retrieval performance data
└── utils/
    ├── bedrock_client.py         # Bedrock integration
    ├── embeddings_client.py      # Embedding generation (Bedrock or external)
    ├── vector_store.py           # In-memory vector database
    └── retriever.py              # Semantic search & ranking
```

## Features
✅ **Document ingestion** – Load and parse FAQ documents
✅ **Embedding generation** – Create vector embeddings for all documents
✅ **Semantic retrieval** – Find relevant docs using vector similarity
✅ **Context grounding** – Include retrieved docs in LLM prompt
✅ **Multi-turn conversation** – Maintain context while retrieving per turn
✅ **Relevance ranking** – Score and filter retrieved results
✅ **Out-of-scope handling** – Detect questions not in knowledge base
✅ **Claude 3.5 Sonnet** – High-quality retrieval-grounded responses
✅ **Logging & metrics** – Track retrieval performance

## Key Files

### `app.py`
Main application with:
- `FAQRetrievalChatbot` class
- Conversation loop with retrieval
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
