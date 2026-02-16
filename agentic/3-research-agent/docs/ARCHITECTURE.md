# Architecture: Research Agent

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
