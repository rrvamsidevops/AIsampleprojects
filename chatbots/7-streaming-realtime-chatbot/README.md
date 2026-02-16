# Streaming/Real-time Chatbot

## Overview
A chatbot optimized for token streaming with progressive response generation, enabling real-time response display to users. Built with AWS Bedrock (Claude 3.5 Sonnet) streaming API.

## Purpose
This application demonstrates streaming and performance optimization:
- Token-by-token streaming responses
- Progressive response display
- Real-time latency measurements
- Cost optimization per token
- Connection management
- Error handling during streaming
- Concurrent user handling

## Application Structure
```
7-streaming-realtime-chatbot/
├── README.md
├── requirements.txt
├── app.py
├── config.py
├── streaming/
│   ├── stream_handler.py       # Streaming response handler
│   ├── token_counter.py        # Token counting & cost
│   ├── stream_buffering.py     # Buffering & batching
│   └── connection_manager.py   # Connection lifecycle
├── prompts/
│   ├── system_prompt.txt       # Streaming-optimized instructions
│   └── examples.json
├── monitoring/
│   ├── latency_tracker.py      # P95, P99 latency
│   ├── token_metrics.py        # Tokens per response
│   ├── cost_calculator.py      # Cost per request
│   └── performance_monitor.py  # Real-time metrics
├── data/
│   └── performance_samples.json
└── utils/
    ├── bedrock_streaming_client.py
    └── metrics.py
```

## Features
✅ Token streaming from Bedrock
✅ Real-time response display
✅ Progressive rendering
✅ Latency measurement (P50, P95, P99)
✅ Token counting and cost tracking
✅ Connection resilience
✅ Error recovery during stream
✅ Concurrent user support
✅ Performance dashboard

## Streaming Architecture
```
User Message
    ↓
[Call Bedrock Stream API]
    ↓
[Receive tokens progressively]
    ↓
[Buffer & send to user]
    ↓
[Display in real-time]
    ↓
[Complete response]
    ↓
[Calculate latency & cost]
```

## Performance Metrics Tracked
- **Latency**: Time to first token, total response time
- **Tokens**: Input tokens, output tokens, total
- **Cost**: Per-token cost, total cost per request
- **Throughput**: Tokens per second
- **Concurrency**: Max concurrent streams

## Testing Focus (Later)
- **Streaming correctness** – Responses complete and coherent?
- **First token latency** – Time to first token P95/P99?
- **Total latency** – Full response time P95/P99?
- **Token accuracy** – Correct token counting?
- **Cost accuracy** – Accurate cost calculation?
- **Connection stability** – Handles interruptions?
- **Error recovery** – Graceful failure during stream?
- **Concurrent users** – Multiple users simultaneously?
- **Memory efficiency** – Buffering doesn't consume too much memory?
- **Throughput** – Tokens/second sustainable?

---

**Status:** Folder structure created, awaiting implementation

---

**Performance Benchmarks to Measure:**
- First token latency target: < 500ms
- Full response latency target: < 5 seconds
- Tokens/second: > 20
- Connection uptime: > 99.9%
- Concurrent users: > 100
