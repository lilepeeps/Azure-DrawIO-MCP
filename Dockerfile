FROM python:3.12-slim

WORKDIR /app

# Copy package definition files
COPY pyproject.toml README.md ./

# Copy server code
COPY azure_drawio_mcp_server/ ./azure_drawio_mcp_server/

# Install the package and its dependencies
RUN pip install --no-cache-dir .

# The MCP server communicates via stdin/stdout
# No ports needed - MCP uses stdio protocol
ENTRYPOINT ["python", "-m", "azure_drawio_mcp_server.server"]
