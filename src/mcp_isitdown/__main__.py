"""
Main entry point for the MCP isitdown server.
"""

from mcp_isitdown.server import mcp


def main() -> None:
    """Run the MCP server with stdio transport."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
