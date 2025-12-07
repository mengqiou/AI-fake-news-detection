# Utilities

Helper functions and utilities for the application.

## `pretty_print.py` - Agent Execution Trace Formatter

Pretty print agent execution traces showing AI messages, tool calls, and results.

### Quick Start

```python
from app.utils.pretty_print import print_agent_execution

# After running agent
final_state = agent.invoke(initial_state)

# Print everything
print_agent_execution(final_state)
```

### Main Functions

#### `print_agent_execution(final_state, ...)`
**The main function** - prints complete execution trace.

```python
from app.utils.pretty_print import print_agent_execution

final_state = agent.invoke(initial_state)

# Full trace (default)
print_agent_execution(final_state)

# Customize what to show
print_agent_execution(
    final_state,
    show_summary=True,      # Execution summary
    show_tools=True,        # Tool calls and results
    show_messages=True,     # Message history
    show_final=True,        # Final response
    truncate_length=500     # Max message length
)
```

**Output Example:**
```
==================================================================
EXECUTION SUMMARY
==================================================================

Total Iterations: 3
Total Messages: 4
Tool Calls: 1

==================================================================
TOOL EXECUTION HISTORY
==================================================================

[Tool Call 1]
Tool: verify_on_platform

Output:
❌ Status: FALSE
Verified By: CDC, WHO, FDA
...
----------------------------------------------------------------------

==================================================================
MESSAGE HISTORY (Agent's Thinking)
==================================================================

👤 [Message 1] HumanMessage
Please analyze this news...
----------------------------------------------------------------------

🤖 [Message 2] AIMessage
I'll verify this claim...

🔧 Tool Calls Requested: 1
  • verify_on_platform
    Args: {'claim': 'bleach cures COVID'}
----------------------------------------------------------------------

🔧 [Message 3] ToolMessage
❌ Status: FALSE...
----------------------------------------------------------------------

🤖 [Message 4] AIMessage
Based on verification: This is dangerous misinformation...
----------------------------------------------------------------------

==================================================================
FINAL AGENT RESPONSE
==================================================================
Platform Verification: FALSE
Credibility Score: 0/100
...
==================================================================
```

#### `print_compact_execution(final_state)`
**Compact version** - summary and final response only.

```python
from app.utils.pretty_print import print_compact_execution

final_state = agent.invoke(initial_state)
print_compact_execution(final_state)
```

**Output:**
```
==================================================================
EXECUTION SUMMARY
==================================================================
Total Iterations: 3
Total Messages: 4
Tool Calls: 1

==================================================================
FINAL AGENT RESPONSE
==================================================================
[Final response text...]
==================================================================
```

#### `print_tools_only(final_state)`
**Tools only** - just show tool execution history.

```python
from app.utils.pretty_print import print_tools_only

final_state = agent.invoke(initial_state)
print_tools_only(final_state)
```

### Individual Component Functions

For custom formatting, use individual functions:

```python
from app.utils.pretty_print import (
    print_execution_summary,
    print_tool_history,
    print_message_history,
    print_final_response,
    print_message,
    print_section,
    print_separator
)

final_state = agent.invoke(initial_state)

# Print components individually
print_execution_summary(final_state)
print_tool_history(final_state)
print_message_history(final_state, truncate_length=300)
print_final_response(final_state)

# Or use formatting helpers
print_section("MY CUSTOM SECTION")
print("Content here...")
print_separator()
```

### Message Type Emojis

Messages are automatically formatted with emojis:
- 👤 `HumanMessage` - User input
- 🤖 `AIMessage` - Agent response
- 🔧 `ToolMessage` - Tool execution result
- ⚙️ `SystemMessage` - System instructions

### Truncation

Long messages are automatically truncated:

```python
# Default: 500 characters
print_agent_execution(final_state)

# Custom truncation
print_agent_execution(final_state, truncate_length=200)

# No truncation
print_agent_execution(final_state, truncate_length=999999)
```

When truncated, shows:
```
Content here is very long and goes on and on...
[truncated, 1523 chars total]
```

### Usage in Tests

#### Verbose Test
```python
# tests/quick_test_verbose.py
from app.utils.pretty_print import print_agent_execution

final_state = agent.invoke(initial_state)
print_agent_execution(final_state)
```

#### Regular Test
```python
# tests/quick_test.py
from app.utils.pretty_print import print_compact_execution

final_state = agent.invoke(initial_state)
print_compact_execution(final_state)
```

#### Custom Test
```python
from app.utils.pretty_print import print_section, print_tool_history

print_section("MY TEST")
final_state = agent.invoke(initial_state)
print_tool_history(final_state)  # Just show tools
```

### Aliases

Convenience aliases for shorter code:

```python
from app.utils.pretty_print import pretty_print, compact_print

# Same as print_agent_execution
pretty_print(final_state)

# Same as print_compact_execution
compact_print(final_state)
```

## Other Utilities

### `config_utils.py`
Agent configuration utilities.

```python
from app.utils.config_utils import get_agent_by_config_id

agent_config = get_agent_by_config_id("fake-news-detector-v1")
```

## Adding New Utilities

When adding new utilities:

1. **Create module** in `app/utils/`
2. **Add docstrings** for all functions
3. **Update this README** with usage examples
4. **Write tests** if complex logic
5. **Keep utilities pure** - no side effects, no state

Example structure:
```python
"""
Brief description of what this utility does.
"""

from typing import Any


def my_utility_function(input: Any) -> Any:
    """
    What this function does.
    
    Args:
        input: Description
        
    Returns:
        Description
        
    Example:
        ```python
        result = my_utility_function("test")
        ```
    """
    # Implementation
    pass
```
