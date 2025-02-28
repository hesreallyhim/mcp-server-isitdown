# MCP IsItDown Service

An MCP server that checks if a website is currently down by querying [isitdownrightnow.com](https://www.isitdownrightnow.com).

## Installation

```bash
# Using uv (recommended)
uv pip install -e .

# Using pip
pip install -e .
```

## Usage

### Run as a standalone MCP server

```bash
# Using the installed script
mcp-isitdown

# Using the Python module
python -m mcp_isitdown

# Using MCP CLI
mcp run -m mcp_isitdown
```

### Use as a library

```python
from mcp_isitdown.server import get_website_status

# You can import the MCP server functions directly
result = await get_website_status("example.com")
```

## Development

```bash
# Type checking
pyright

# Install in development mode
uv pip install -e .
```

## License

MIT
