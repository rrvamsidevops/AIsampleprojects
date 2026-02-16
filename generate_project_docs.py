#!/usr/bin/env python3
"""
Generate project-specific documentation for all QA platform projects.
This script auto-generates SETUP.md, TESTING.md, and ARCHITECTURE.md for each project
based on project type (chatbot, RAG, agentic) and project metadata.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Define project categories and their characteristics
PROJECT_CATEGORIES = {
    "chatbots": {
        "type": "chatbot",
        "description": "Conversational AI applications",
        "common_deps": ["boto3>=1.28.0", "python-dotenv"],
        "model": "Claude 3.5 Sonnet via AWS Bedrock",
    },
    "RAG": {
        "type": "rag",
        "description": "Retrieval-Augmented Generation systems",
        "common_deps": ["boto3>=1.28.0", "python-dotenv", "requests", "PyPDF2"],
        "model": "Claude 3.5 Sonnet via AWS Bedrock + Vector Store",
    },
    "agentic": {
        "type": "agentic",
        "description": "Agentic AI workflows with tool use",
        "common_deps": ["boto3>=1.28.0", "python-dotenv"],
        "model": "Claude 3.5 Sonnet via AWS Bedrock + Tool calling",
    },
}

def get_project_name_and_category(readme_path: Path) -> Tuple[str, str, str]:
    """Extract project name and category from README.md"""
    if not readme_path.exists():
        return "Unknown Project", "", ""
    
    content = readme_path.read_text()
    name_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    project_name = name_match.group(1) if name_match else "Unknown Project"
    return project_name, ""


def get_project_type(project_path: Path) -> str:
    """Determine project type based on folder hierarchy"""
    parts = project_path.parts
    for part in parts:
        if part in PROJECT_CATEGORIES:
            return PROJECT_CATEGORIES[part]["type"]
    return "unknown"


def generate_setup_md(project_path: Path, project_name: str, project_type: str) -> str:
    """Generate SETUP.md content"""
    category_info = PROJECT_CATEGORIES.get(
        next((part for part in project_path.parts if part in PROJECT_CATEGORIES), None),
        {"common_deps": []},
    )
    deps_json = json.dumps(category_info['common_deps'], indent=2)
    
    content = f"""# Setup Guide: {project_name}

## Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- AWS Account with Bedrock access
- `.env` file with AWS credentials

## Installation Steps

### 1. Create Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\\Scripts\\activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure AWS Credentials
Create a `.env` file in the project root:
```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

Or use AWS CLI configuration:
```bash
aws configure
```

### 4. Verify Installation
```bash
source venv/bin/activate  # macOS/Linux
# OR
venv\\Scripts\\activate  # Windows

python -m pytest test_*.py -v
```

## Running the Application

### Interactive Mode
```bash
source venv/bin/activate
python app.py
```

### With Logging
```bash
export LOG_LEVEL=DEBUG  # macOS/Linux
# OR
set LOG_LEVEL=DEBUG  # Windows
python app.py
```

## Troubleshooting

### "No module named 'boto3'"
- Ensure venv is activated: `source venv/bin/activate`
- Reinstall requirements: `pip install -r requirements.txt`

### AWS Credentials Error
- Verify `.env` file exists and has correct credentials
- Check AWS_REGION is set to `us-east-1`
- Run: `aws sts get-caller-identity` to verify AWS access

### Bedrock Model Not Found
- Confirm Bedrock is available in your AWS region (us-east-1 recommended)
- Check IAM permissions for `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream`

## Project Dependencies
```
{deps_json}
```

See `requirements.txt` for the complete dependency list.
"""
    return content


def generate_testing_md(project_path: Path, project_name: str, project_type: str) -> str:
    """Generate TESTING.md content"""
    
    if project_type == "chatbot":
        focus = """### Unit Tests (`test_chatbot.py`)
- Initialization and configuration loading
- System prompt validation
- Conversation history management
- Input/output formatting
- Error handling for malformed inputs

### Integration Tests (`test_integration.py`)
- Actual AWS Bedrock API calls
- Multi-turn conversation flow
- Token counting accuracy
- Error handling for AWS failures

### Manual Testing
```bash
source venv/bin/activate
python app.py
```"""
    elif project_type == "rag":
        focus = """### Unit Tests (`test_rag.py`)
- Document loading and parsing
- Chunk creation and splitting
- Vector embedding format
- Retrieval query formatting
- Memory management with large documents

### Integration Tests (`test_integration.py`)
- End-to-end document retrieval
- Semantic search quality
- Response generation with retrieved context
- AWS Bedrock API with embeddings

### Manual Testing
```bash
source venv/bin/activate
python app.py
```"""
    elif project_type == "agentic":
        focus = """### Unit Tests (`test_agent.py`)
- Tool registration and validation
- Tool schema generation
- Agent state management
- Action parsing from LLM responses
- Error handling for invalid tool calls

### Integration Tests (`test_integration.py`)
- Full agent workflow execution
- Multi-step tool use
- Proper error recovery
- AWS Bedrock API with tool use
- Complex multi-turn agent interactions

### Manual Testing
```bash
source venv/bin/activate
python app.py
```"""
    else:
        focus = """### Unit Tests
- Core functionality validation
- Configuration loading
- Error handling

### Integration Tests  
- AWS Bedrock API integration
- End-to-end workflow

### Manual Testing
```bash
source venv/bin/activate
python app.py
```"""

    content = f"""# Testing Guide: {project_name}

## Overview
Testing strategy for this project, including unit tests, integration tests, and manual testing.

## Test Structure

```
tests/
├── __init__.py
├── test_*.py          # Unit tests
└── test_integration.py # Integration tests with AWS
```

## Running Tests

### Run All Tests
```bash
source venv/bin/activate
python -m pytest -v
```

### Run Specific Test File
```bash
python -m pytest test_chatbot.py -v
```

### Run with Coverage Report
```bash
pip install pytest-cov
python -m pytest --cov=. --cov-report=html
```

## Test Types

{focus}

## Unit vs Integration Tests

| Aspect | Unit Tests | Integration Tests |
|--------|------------|------------------|
| **Speed** | Fast (milliseconds) | Slower (seconds) |
| **AWS Access** | Not required | Requires AWS credentials |
| **Scope** | Single function/class | Full workflow |
| **Frequency** | Run often (on save) | Run before commit |
| **Cost** | Free | Small AWS charges |
| **Dependencies** | Minimal | AWS Bedrock required |

## AWS Permissions Required

For integration tests to pass, ensure your AWS user has bedrock permissions:
```json
{{
  "Effect": "Allow",
  "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
  "Resource": "arn:aws:bedrock:us-east-1::foundation-model/*"
}}
```

## Debugging Tests

### Enable Debug Logging
```bash
export LOG_LEVEL=DEBUG
python -m pytest test_integration.py -v -s
```

### Run Single Test
```bash
python -m pytest test_chatbot.py::test_initialization -v
```

### Skip Integration Tests (offline mode)
```bash
python -m pytest -v -m "not integration"
```

## Best Practices

1. Run unit tests frequently during development
2. Run integration tests before commits to main branch
3. Mock AWS calls in unit tests to keep them fast
4. Track test coverage and aim for >80%
5. Write tests for edge cases not just happy paths
6. Use descriptive test names that explain what is being tested

## Common Issues

### Tests Fail with "No module named 'boto3'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### AWS Credentials Error in Integration Tests
- Verify `.env` file exists with valid credentials
- Run: `aws sts get-caller-identity`
- Check IAM user has `bedrock:InvokeModel` permission

### Tests Pass Locally but Fail in CI/CD
- Ensure AWS_REGION is set to `us-east-1`
- Verify environment variables are set in CI/CD pipeline
- Check IAM role has required Bedrock permissions
"""
    return content


def generate_architecture_md(project_path: Path, project_name: str, project_type: str) -> str:
    """Generate ARCHITECTURE.md content"""
    
    if project_type == "chatbot":
        content = f"""# Architecture: {project_name}

## System Overview

Multi-turn conversational chatbot that maintains context and history across interactions.

## Key Components

1. **app.py** - Main chatbot orchestration
2. **utils/bedrock_client.py** - AWS Bedrock wrapper
3. **config.py** - Centralized configuration
4. **prompts/** - System prompts and examples

## Core Features

- **Multi-turn conversations**: Maintains context across turns
- **History management**: Tracks and trims conversation history
- **Error handling**: Graceful failure recovery
- **Logging**: All interactions logged for debugging

## Data Flow

User Input → Message Formatting → Bedrock API (Claude) → Response Formatting → User Output

## Context Management

- Keeps last 10 conversation turns
- Trims history when approaching token limits
- Preserves conversation coherence

## Error Handling

1. Connection errors → Retry with backoff
2. Invalid inputs → Validate before API call
3. AWS failures → Log and alert user

## Performance Configuration

- Temperature: 0.7 (balanced creativity)
- Max tokens: 1000 (sufficient responses)
- Region: us-east-1
- Model: Claude 3.5 Sonnet

## Security

- Credentials stored in `.env` file
- No sensitive data in logs
- Input validation before API calls
- History kept in-memory (not persisted)

See [SETUP.md](SETUP.md) for detailed setup instructions.
"""

    elif project_type == "rag":
        content = f"""# Architecture: {project_name}

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
"""

    elif project_type == "agentic":
        content = f"""# Architecture: {project_name}

## System Overview

Agentic workflow system where Claude acts as a decision-maker, choosing and executing tools as needed.

## Agent Loop

```
1. [LLM Decision] - Claude decides which tool to use
2. [Tool Parsing] - Extract tool name and parameters
3. [Validation] - Verify tool and parameter validity
4. [Execution] - Run the tool
5. [Result Processing] - Format result as observation
6. [Termination Check] - Done? Or loop again?
```

## Key Components

1. **app.py** - Agent orchestration and loop
2. **tools/base_tool.py** - Base tool abstraction
3. **tools/** - Individual tool implementations
4. **utils/bedrock_client.py** - Claude with tool use

## Tool Use Mechanism

Claude receives:
- Tool name and description
- Input schema (parameters)
- Expected output format

Claude responds with:
- Tool name to invoke
- Parameters to pass
- Reasoning for the choice

Agent then:
- Validates the tool call
- Executes the tool
- Returns result to Claude
- Loops until done

## Tool Schema Definition

Tools define:
```
- name: Unique identifier
- description: What the tool does
- parameters: Input schema
- execute(): Implementation
```

## Agent Safety

1. **Input Validation** - Type and constraint checking
2. **Execution Guards** - Timeout and rate limiting
3. **Permission Checks** - Authorization validation
4. **Output Sanitization** - Hide sensitive data

## Error Recovery

- Invalid tool calls: Claude self-corrects
- Tool failures: Formatted as error observations
- Max iterations: Prevents infinite loops
- Malformed responses: Graceful degradation

## State Management

- Conversation history tracked
- Tool results accumulated
- Action trace logged for debugging
- Context managed to stay within limits

## Metrics to Track

1. Average tools per request (efficiency)
2. Tool success rate (reliability)
3. Iterations before completion (control)
4. Total execution time (performance)

## Debugging

- Action trace shows full reasoning path
- Step-through mode for inspection
- Tool output validation
- LLM response inspection

See [SETUP.md](SETUP.md) for detailed setup instructions.
"""

    else:
        content = f"""# Architecture: {project_name}

## System Overview

This project demonstrates a practical AI Quality Engineering implementation using AWS Bedrock and Claude 3.5 Sonnet.

## Key Components

1. **app.py** - Main application logic
2. **utils/bedrock_client.py** - AWS Bedrock integration
3. **config.py** - Configuration and constants
4. **prompts/** - System prompts and examples

## Data Flow

User Input → Validation → Bedrock API → Response Processing → User Output

## Error Handling

- Connection errors: Retry with backoff
- Invalid inputs: Validate before API call
- AWS failures: Log and notify user

## Performance Configuration

- Temperature: 0.7 (balanced creativity)
- Max tokens: 1000 (sufficient responses)
- Region: us-east-1
- Model: Claude 3.5 Sonnet

## AWS Configuration

- Bedrock Runtime API
- Claude 3.5 Sonnet model
- us-east-1 region (recommended)

## Security Considerations

- AWS credentials in `.env` file
- Input validation before API calls
- Error logging without exposing credentials
- No sensitive data persistence

See [SETUP.md](SETUP.md) for detailed setup instructions.
"""

    return content


def generate_docs_for_project(project_path: Path) -> bool:
    """Generate all doc files for a single project"""
    docs_dir = project_path / "docs"
    readme_path = project_path / "README.md"
    
    if not readme_path.exists():
        return False
    
    docs_dir.mkdir(exist_ok=True)
    
    project_name = get_project_name_and_category(readme_path)[0]
    project_type = get_project_type(project_path)
    
    docs = {
        "SETUP.md": generate_setup_md(project_path, project_name, project_type),
        "TESTING.md": generate_testing_md(project_path, project_name, project_type),
        "ARCHITECTURE.md": generate_architecture_md(project_path, project_name, project_type),
    }
    
    for filename, content in docs.items():
        (docs_dir / filename).write_text(content)
    
    return True


def main():
    """Main entry point"""
    base_dir = Path(__file__).parent
    
    print("🚀 Generating project-specific documentation...\n")
    
    projects = []
    for category_dir in sorted(base_dir.iterdir()):
        if category_dir.name in PROJECT_CATEGORIES and category_dir.is_dir():
            for project_dir in sorted(category_dir.iterdir()):
                if project_dir.is_dir() and not project_dir.name.startswith('.'):
                    projects.append(project_dir)
    
    success_count = 0
    skip_count = 0
    
    print(f"📋 Found {len(projects)} projects\n")
    
    for project_path in projects:
        category = next(p for p in project_path.parts if p in PROJECT_CATEGORIES)
        project_type = PROJECT_CATEGORIES[category]["type"]
        
        if generate_docs_for_project(project_path):
            print(f"✅ {category}/{project_path.name:40} ({project_type})")
            success_count += 1
        else:
            print(f"⏭️  {category}/{project_path.name:40} (skipped - no README)")
            skip_count += 1
    
    print(f"\n{'='*70}")
    print(f"📊 Summary:")
    print(f"   ✅ Generated docs for {success_count} projects")
    print(f"   ⏭️  Skipped {skip_count} projects")
    print(f"   📁 Created: SETUP.md, TESTING.md, ARCHITECTURE.md")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
