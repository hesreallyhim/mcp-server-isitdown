# Generated by https://smithery.ai. See: https://smithery.ai/docs/config#dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim

# ensure stdout/stderr are unbuffered
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# copy pyproject and source
COPY pyproject.toml .
COPY src ./src

# install dependencies and the package
RUN pip install --no-cache-dir .

# default entrypoint for MCP server
ENTRYPOINT ["mcp-server-isitdown"]
