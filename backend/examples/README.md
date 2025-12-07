# Examples

Code examples demonstrating how to use various components of the system.

## Available Examples

### `pretty_print_example.py`
**Pretty Print Utility Usage**

Shows different ways to format and display agent execution traces.

```bash
python examples/pretty_print_example.py
```

**What it demonstrates:**
1. **Full trace** - Complete execution with all details
2. **Compact output** - Summary and final response only
3. **Tools only** - Just tool execution history
4. **Custom combination** - Mix and match what to show

**Interactive:**
- Choose which example to run
- See different formatting options
- Learn the pretty_print API

## Usage

All examples are standalone scripts:

```bash
cd backend
python examples/<example_name>.py
```

## Prerequisites

- Agent deployed: `python scripts/update_config.py all fake_news_detector_v1`
- AWS configured: Credentials in `.env`
- Dependencies installed: `pip install -r requirements.txt`

## Creating New Examples

When adding examples:

1. **Create script** in `examples/`
2. **Add docstring** at top explaining what it demonstrates
3. **Make it interactive** if helpful (let user choose options)
4. **Update this README** with description
5. **Keep it simple** - one concept per example

Example template:

```python
"""
Example: Brief description of what this demonstrates.
"""

import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Your example code here

def main():
    """Main example function."""
    print("Example: What it does")
    # Implementation

if __name__ == "__main__":
    main()
```

## Example Ideas

Potential future examples:

- **Custom tool creation** - How to add new tools
- **Sub-agent architecture** - Hierarchical agents
- **Streaming responses** - Real-time output
- **Error handling** - Robust agent workflows
- **RAG integration** - Using knowledge base
- **Multi-turn conversation** - Stateful agents
- **Batch processing** - Process multiple articles
- **Custom prompts** - Different prompt strategies
