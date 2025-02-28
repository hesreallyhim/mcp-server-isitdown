# mcp-server-isitdown Project Guidelines

## Build & Development Commands
- Run the server: `uv run isitdown.py`
- Type checking: `pyright` or `pyright isitdown.py`
- Install dependencies: `uv pip install -e .`

Note: `uv` is the preferred tool for this project for running Python and managing dependencies

## Version Control
- Always use conventional commits for commit messages (feat:, fix:, docs:, chore:, etc.)
- Follow the pattern: type(scope): description

## Project Knowledge
- Key documentation snippets will be added directly to this file
- For extensive documentation, specific files will be referenced by absolute path
- At the bottom is a summarized version of the MCP Python SDK README, including `FastMCP`.

## Code Style Guidelines
- Python 3.12+ compatible code
- Type hints required for all functions and parameters
- Docstrings for all public functions using Google style
- Error handling: Use try/except with specific exceptions
- Variable naming: snake_case for variables and functions
- Constants in UPPER_CASE
- Class names in PascalCase
- Use f-strings for string formatting
- Import order: standard library, third-party, local modules
- Line length: 88 characters maximum
- Error messages should be informative and actionable

# MCP Python SDK Summary

## Core Concepts

### Installation
```bash
# Recommended: using uv
uv add "mcp[cli]"

# Alternative: using pip
pip install mcp
```

### FastMCP Server
```python
from mcp.server.fastmcp import FastMCP

# Basic server creation
mcp = FastMCP("ServerName")

# With dependencies
mcp = FastMCP("ServerName", dependencies=["pandas", "numpy"])

# With lifespan context
@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    try:
        # Initialize on startup
        await db.connect()
        yield {"db": db}  # Context accessible in tools/resources
    finally:
        # Cleanup on shutdown
        await db.disconnect()

mcp = FastMCP("ServerName", lifespan=app_lifespan)
```

### Resources (Data Access)
```python
# Static resource
@mcp.resource("config://app")
def get_config() -> str:
    """Static configuration data"""
    return "App configuration here"

# Dynamic resource with parameters
@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    """Dynamic user data"""
    return f"Profile data for user {user_id}"
```

### Tools (Actions/Computation)
```python
# Simple tool
@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m ** 2)

# Async tool
@mcp.tool()
async def fetch_data(query: str, ctx: Context) -> str:
    """Fetch data with progress reporting"""
    ctx.info(f"Processing query: {query}")
    await ctx.report_progress(0, 1)
    # Perform action
    await ctx.report_progress(1, 1)
    return "Result"
```

### Prompts (Templates)
```python
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"

@mcp.prompt()
def debug_error(error: str) -> list[Message]:
    return [
        UserMessage("I'm seeing this error:"),
        UserMessage(error),
        AssistantMessage("I'll help debug that. What have you tried so far?")
    ]
```

### Working with Images
```python
from mcp.server.fastmcp import FastMCP, Image

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")
```

### Context Object
The Context object gives access to MCP capabilities:
```python
@mcp.tool()
async def process_file(file_path: str, ctx: Context) -> str:
    # Log message to client
    ctx.info(f"Processing {file_path}")

    # Report progress
    await ctx.report_progress(0, 1)

    # Read another resource
    data, mime_type = await ctx.read_resource(f"file://{file_path}")

    # Access lifespan context
    db = ctx.request_context.lifespan_context["db"]

    return "Processing complete"
```

## Running a Server

### Development Mode
```bash
mcp dev server.py
mcp dev server.py --with pandas --with numpy
mcp dev server.py --with-editable .
```

### Claude Desktop Integration
```bash
mcp install server.py
mcp install server.py --name "Custom Server Name"
mcp install server.py -v API_KEY=abc123 -v DB_URL=postgres://...
```

### Direct Execution
```python
if __name__ == "__main__":
    mcp.run()
```
```bash
python server.py
# or
mcp run server.py
```

## MCP Primitives

| Primitive | Control | Description | Example Use |
|-----------|---------|-------------|-------------|
| Prompts | User-controlled | Templates invoked by user choice | Slash commands, menu options |
| Resources | App-controlled | Contextual data managed by client | File contents, API responses |
| Tools | Model-controlled | Functions for LLM to take actions | API calls, data updates |
