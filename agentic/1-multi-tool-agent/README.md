# Multi-Tool Agent

## Overview
An agentic AI system that orchestrates multiple tools (search, booking, cancellation, payment) to complete complex user requests autonomously. Built with AWS Bedrock (Claude 3.5 Sonnet) using function calling and agentic reasoning loops.

## Purpose
This application demonstrates **agentic AI workflows** with:
- Autonomous tool selection and invocation
- Chain-of-thought reasoning over multiple steps
- Agent loop with observation and reflection
- Tool result integration into context
- State management across multi-step workflows
- Graceful failure recovery and loop detection
- Human-in-the-loop escalation

## Application Structure
```
1-multi-tool-agent/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── app.py                         # Main agent application
├── config.py                      # Configuration & constants
├── agent/
│   ├── __init__.py
│   ├── agent.py                  # Core Agent class
│   ├── reasoning_loop.py          # Agent loop orchestration
│   └── tool_executor.py           # Executes selected tools
├── tools/
│   ├── __init__.py
│   ├── base_tool.py              # Abstract tool interface
│   ├── search_tool.py            # Search knowledge base
│   ├── booking_tool.py           # Create bookings
│   ├── cancellation_tool.py      # Cancel bookings
│   ├── payment_tool.py           # Process payments
│   └── escalation_tool.py        # Escalate to human
├── prompts/
│   ├── system_prompt.txt         # Agent system instructions
│   ├── tool_definitions.json     # Tool specs (for function calling)
│   ├── reasoning_prompt.txt      # Chain-of-thought prompt
│   └── examples.json             # Few-shot agent examples
├── data/
│   ├── user_database.json        # Mock user data
│   ├── booking_database.json     # Mock bookings
│   └── sample_workflows.json     # Example multi-step workflows
├── logs/
│   ├── agent.log                # Agent execution logs
│   └── tool_calls.log           # Detailed tool call logs
└── utils/
    ├── bedrock_client.py         # Bedrock integration
    ├── state_manager.py          # Agent state tracking
    ├── loop_detector.py          # Detect infinite loops
    └── metrics.py                # Agent performance metrics
```

## Features
✅ **Tool orchestration** – Autonomous selection & invocation of tools
✅ **Function calling** – Uses Claude's tool use capability
✅ **Agent loop** – Think → Act → Observe → Reflect cycle
✅ **Chain-of-thought** – Transparent reasoning for each step
✅ **Multi-step workflows** – Sequences multiple tools (e.g., search → book → pay)
✅ **Tool result integration** – Incorporates results back into reasoning
✅ **Loop detection** – Detects infinite loops and breaks them
✅ **State management** – Tracks agent context and intermediate results
✅ **Error recovery** – Handles tool failures gracefully
✅ **Escalation** – Escalates to humans for critical decisions
✅ **Claude 3.5 Sonnet** – Superior reasoning and tool selection

## Key Files

### `app.py`
Main application with:
- `Agent` class initialization
- User request entry point
- Agent loop orchestration call
- Final response formatting

### `agent/agent.py`
Core agent class:
- `think()` – Generate next action via Claude
- `act()` – Execute selected tool
- `observe()` – Process tool result
- `reflect()` – Update internal state
- `execute()` – Full reasoning loop

### `agent/reasoning_loop.py`
Orchestrates the agent loop:
- Max iterations limit (prevent infinite loops)
- Step-by-step execution
- Context window management
- Early exit conditions

### `tools/base_tool.py`
Abstract tool interface:
```python
class BaseTool:
    def execute(self, **kwargs) -> str:
        pass
    
    def validate_inputs(self, **kwargs) -> bool:
        pass
```

### `tools/search_tool.py`, `booking_tool.py`, etc.
Concrete tool implementations for different actions.

### `prompts/tool_definitions.json`
Tool specifications in Claude function-calling format:
```json
{
  "tools": [
    {
      "name": "search_bookings",
      "description": "Search available bookings",
      "input_schema": {...}
    },
    {
      "name": "create_booking",
      "description": "Create a new booking",
      "input_schema": {...}
    }
  ]
}
```

### `utils/loop_detector.py`
Prevents infinite loops:
- Track tool calls across iterations
- Detect repeated tool calls
- Break loops after max iterations

## Prerequisites
- AWS Bedrock access (Claude 3.5 Sonnet with function calling)
- AWS credentials configured
- Python 3.9+

## Installation & Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure

# Run the agent
python app.py
```

## How It Works
**Example: User says "I want to book a flight and pay for it"**

1. **Think** – Claude analyzes request, selects "search_flights" tool
2. **Act** – Execute search_flights with parameters
3. **Observe** – Get available flights from tool
4. **Reflect** – Update reasoning with flight options
5. **Think** – Claude selects "create_booking" based on results
6. **Act** – Execute booking creation
7. **Observe** – Get booking confirmation
8. **Reflect** – Update state with booking ID
9. **Think** – Claude selects "process_payment" tool
10. **Act** – Process payment with booking ID
11. **Observe** – Get payment confirmation
12. **Reflect** – Mark workflow as complete
13. **Response** – Return final summary to user

## Sample Agent Tasks
- "Book me a flight to NYC next week and process payment"
- "Find my recent booking and cancel it"
- "What flights are available tomorrow? Book the cheapest one"
- "I need to change my payment method for booking ABC123"

## Agent Loop Diagram
```
User Request
    ↓
[THINK] Claude decides next tool
    ↓
[ACT] Execute selected tool
    ↓
[OBSERVE] Get tool result
    ↓
[REFLECT] Update internal state
    ↓
Goal reached? ─YES→ Generate final response
    ↓ NO
Max iterations? ─YES→ Escalate to human
    ↓ NO
Infinite loop? ─YES→ Break loop, escalate
    ↓ NO
[THINK] Continue reasoning...
```

## Testing & Validation (Later Phases)
This application will be evaluated for:
- **Tool selection accuracy** – Correct tool chosen for task?
- **Tool parameter correctness** – Valid arguments passed?
- **Chain-of-thought stability** – Consistent reasoning across runs?
- **Loop detection** – Infinite loops caught and stopped?
- **Failure recovery** – Graceful handling of tool errors?
- **State consistency** – Correct state tracked across steps?
- **Multi-step completion** – Complex workflows finished successfully?
- **Escalation appropriateness** – Human involved when needed?
- **Latency** – Total execution time for multi-step workflows?
- **Cost** – Token usage per workflow?

---

**Next Step:** Build agent loop logic and tool implementations
