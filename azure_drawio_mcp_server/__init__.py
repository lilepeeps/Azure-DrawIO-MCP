# Copyright (c) 2026. Inspired by dminkovski/azure-diagram-mcp
"""Azure Draw.io MCP Server - Generate editable Draw.io diagrams for Azure architectures."""

__version__ = "0.1.0"

from azure_drawio_mcp_server.validator import (
    validate_drawio_file,
    validate_drawio_content,
    format_validation_result,
)

__all__ = [
    "validate_drawio_file",
    "validate_drawio_content", 
    "format_validation_result",
]
