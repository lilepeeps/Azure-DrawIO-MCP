# Copyright (c) 2026. Inspired by dminkovski/azure-diagram-mcp
"""Pydantic models for the azure-drawio-mcp-server."""

from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Optional


class DiagramType(str, Enum):
    """Enum for supported diagram types."""
    AZURE = 'azure'
    NETWORK = 'network'
    COMPUTE = 'compute'
    DATA = 'data'
    INTEGRATION = 'integration'
    SECURITY = 'security'
    ALL = 'all'


class AzureResource(BaseModel):
    """Model for an Azure resource in a diagram."""
    id: str = Field(..., description='Unique identifier for this resource')
    resource_type: str = Field(..., description='Azure resource type (e.g., VM, AppService, SQLDatabase)')
    name: str = Field(..., description='Display name for the resource')
    x: Optional[int] = Field(None, description='X position (auto-calculated if not provided)')
    y: Optional[int] = Field(None, description='Y position (auto-calculated if not provided)')
    group: Optional[str] = Field(None, description='Optional group/cluster this resource belongs to')
    rationale: Optional[str] = Field(None, description='Optional rationale for including this resource in the architecture')


class Connection(BaseModel):
    """Model for a connection between resources."""
    source: str = Field(..., description='Source resource ID')
    target: str = Field(..., description='Target resource ID')
    label: Optional[str] = Field(None, description='Optional label for the connection')
    style: Optional[str] = Field('solid', description='Line style: solid, dashed, dotted')


class ResourceGroup(BaseModel):
    """Model for a resource group (cluster) in the diagram."""
    id: str = Field(..., description='Unique identifier for this group')
    name: str = Field(..., description='Display name for the group')
    color: Optional[str] = Field(None, description='Background color (hex)')


class DiagramRequest(BaseModel):
    """Request model for diagram generation."""
    title: str = Field(..., description='Diagram title')
    resources: List[AzureResource] = Field(..., description='List of Azure resources to include')
    connections: List[Connection] = Field(default_factory=list, description='List of connections between resources')
    groups: List[ResourceGroup] = Field(default_factory=list, description='Optional resource groups/clusters')
    workspace_dir: Optional[str] = Field(None, description='Workspace directory to save diagrams')
    filename: Optional[str] = Field(None, description='Output filename (without extension)')
    open_in_vscode: bool = Field(False, description='Open the diagram in VS Code after generation (requires hediet.vscode-drawio extension)')
    show_legend: bool = Field(True, description='Show a legend table at the bottom with numbered resources, names, types, and rationale')


class DiagramResponse(BaseModel):
    """Response model for diagram generation."""
    status: Literal['success', 'error']
    path: Optional[str] = None
    message: str
    opened_in_vscode: bool = False


class ShapeInfo(BaseModel):
    """Information about an available Azure shape."""
    resource_type: str = Field(..., description='Resource type identifier')
    display_name: str = Field(..., description='Human-readable name')
    category: str = Field(..., description='Category (compute, network, storage, etc.)')
    style: str = Field(..., description='Draw.io style string')


class ShapesResponse(BaseModel):
    """Response model for listing available shapes."""
    shapes: Dict[str, List[ShapeInfo]]
    total_count: int


class ExampleResponse(BaseModel):
    """Response model for diagram examples."""
    examples: Dict[str, Dict]
