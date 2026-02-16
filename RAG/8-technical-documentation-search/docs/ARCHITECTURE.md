# Architecture: Technical Documentation Search

## System Overview

Retrieval-Augmented Generation system that combines document search with Claude's generation capabilities.

## Pipeline Stages

1. **Document Loading** - Parse and chunk source documents
2. **Embedding** - Convert chunks to vectors via Bedrock Titan
3. **Vector Search** - Find similar chunks for query
4. **Context Assembly** - Combine relevant chunks
5. **LLM Generation** - Claude generates answer with context
6. **Response Formatting** - Add source citations

## Key Components

1. **app.py** - RAG pipeline orchestration
2. **utils/document_loader.py** - Document parsing and chunking
3. **utils/vector_store.py** - Vector embeddings and search
4. **utils/bedrock_client.py** - AWS Bedrock integration

## Retrieval Strategy

- **Chunking**: 512 tokens per chunk with 50-token overlap
- **Search**: Cosine similarity on embeddings
- **Top-K**: Retrieve top 5 similar chunks
- **Threshold**: Minimum similarity score 0.7

## Vector Details

- **Provider**: AWS Bedrock Titan Embeddings
- **Dimensions**: 1536-dimensional vectors
- **Performance**: ~50ms per chunk embedding

## Context Window Management

```
Total: 200,000 tokens (Claude limit)
Reserved: 600 tokens (system + query)
Response: 1,000 tokens
Available for Context: ~198,400 tokens
Typical Usage: ~2,500 tokens (5 chunks)
```

## Hallucination Prevention

1. Always prompt to answer based ONLY on documents
2. Include source citations for verification
3. Log potential hallucinations
4. Add confidence scoring to answers
5. Request user feedback on accuracy

## Error Handling

- No relevant docs: Show disclaimer
- Embedding errors: Fall back to keyword search
- Token overflow: Truncate least relevant chunks
- Generation timeout: Retry or return placeholder

## Scalability

Current: In-memory vector store (~10K docs)
Production: Use vector database (Pinecone, Weaviate, Milvus)

## Metrics to Track

1. Retrieval quality (Precision@5, Recall)
2. Retrieval speed (target <500ms)
3. Answer quality (user satisfaction)
4. Token usage (cost optimization)
5. Hit rate (% of queries with relevant docs)

See [SETUP.md](SETUP.md) for detailed setup instructions.
