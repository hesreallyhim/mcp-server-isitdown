# MCP-isitdown Project Guidelines

## Build & Development Commands
- Run the server: `uv run isitdown.py`
- Type checking: `pyright` or `pyright isitdown.py`
- Install dependencies: `uv pip install -e .`

Note: `uv` is the preferred tool for this project for running Python and managing dependencies

## Version Control
- Always use conventional commits for commit messages (feat:, fix:, docs:, chore:, etc.)
- Follow the pattern: type(scope): description

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