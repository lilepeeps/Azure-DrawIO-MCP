# Copyright (c) 2026. Inspired by dminkovski/azure-diagram-mcp
"""Azure Draw.io MCP Server implementation.

This server provides tools to generate editable Draw.io diagrams for Azure architectures.
Unlike PNG-based diagram generators, the output can be modified in Draw.io or VS Code.
"""

from azure_drawio_mcp_server.drawio_generator import generate_drawio_diagram
from azure_drawio_mcp_server.azure_shapes import list_all_shapes, AZURE_SHAPES, get_shape_info
from azure_drawio_mcp_server.scanner import scan_workspace, DiscoveredResource
from azure_drawio_mcp_server.models import (
    AzureResource,
    Connection,
    ResourceGroup,
    DiagramRequest,
    DiagramResponse,
    ShapesResponse,
    ShapeInfo,
    ExampleResponse,
    DiagramType,
)
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# Create the MCP server
mcp = FastMCP(
    'azure-drawio-mcp-server',
    dependencies=[
        'pydantic',
        'drawpyo',
    ],
    log_level='ERROR',
    instructions="""Use this server to generate editable Draw.io diagrams for Azure architectures.

BENEFITS OVER PNG DIAGRAMS:
- Fully editable: Modify placement, colors, text after generation
- Version control friendly: XML-based format with readable diffs
- VS Code integration: Open directly in VS Code with Draw.io extension
- Export options: Export to PNG, SVG, PDF from Draw.io

BEST PRACTICES - FOLLOW THESE FOR CONSISTENT DIAGRAMS:
1. DO NOT specify x/y coordinates on resources - let the auto-layout engine position them
2. DO NOT use 'style' on connections (no dashed/dotted) - causes errors, use solid lines only
3. ALWAYS include 'rationale' on every resource - this populates the legend with meaningful descriptions
4. ALWAYS use 'groups' to organize resources logically (compute, data, security, etc.)
5. ALWAYS use valid resource_type values from list_azure_shapes tool
6. ALWAYS provide workspace_dir so diagrams save to the user's project

WORKFLOW:
1. list_azure_shapes:
   - Discover all available Azure resource types
   - Browse by category (compute, network, storage, database, etc.)
   - Find the exact resource_type strings to use in your diagrams

2. get_diagram_examples:
   - See example diagram specifications
   - Understand the JSON structure for resources and connections
   - Use examples as templates for your own diagrams

3. generate_diagram:
   - Provide a structured specification with resources and connections
   - Let auto-layout position resources (do NOT specify x/y coordinates)
   - Group related resources into clusters with meaningful colors
   - Include rationale for each resource to populate the legend
   - The diagram is generated as a .drawio file in A4 landscape format
   - Output includes: instructions header, architecture diagram, and legend table

OPENING THE DIAGRAM:
- Install VS Code extension: hediet.vscode-drawio
- Open the .drawio file directly in VS Code
- Or use the Draw.io desktop/web application
"""
)


@mcp.tool(name='generate_diagram')
async def mcp_generate_diagram(
    title: str = Field(..., description='Diagram title'),
    resources: List[dict] = Field(
        ...,
        description='List of Azure resources. Each resource needs: id (unique), resource_type (e.g., VM, AppService), name (display name). Optional: x, y (position), group (group ID)'
    ),
    connections: List[dict] = Field(
        default=[],
        description='List of connections. Each needs: source (resource ID), target (resource ID). Optional: label, style (solid/dashed/dotted)'
    ),
    groups: List[dict] = Field(
        default=[],
        description='Optional resource groups/clusters. Each needs: id, name. Optional: color (hex)'
    ),
    workspace_dir: Optional[str] = Field(
        None,
        description='Workspace directory to save diagrams (creates diagrams/ subfolder)'
    ),
    filename: Optional[str] = Field(
        None,
        description='Output filename (without extension, .drawio added automatically)'
    ),
    open_in_vscode: bool = Field(
        False,
        description='Open the diagram in VS Code after generation (requires hediet.vscode-drawio extension)'
    ),
    show_legend: bool = Field(
        True,
        description='Show a numbered legend table at the bottom of the diagram'
    ),
    use_infinite_canvas: bool = Field(
        False,
        description='Use infinite canvas instead of fixed A4 page. Better for complex diagrams and web docs - no visible page boundaries'
    ),
) -> DiagramResponse:
    """Generate an editable Draw.io diagram for Azure architecture.
    
    Creates a .drawio file that can be opened in VS Code (with Draw.io extension)
    or the Draw.io desktop/web application for further editing.
    """
    # Convert dicts to Pydantic models
    resource_models = [AzureResource(**r) for r in resources]
    connection_models = [Connection(**c) for c in connections]
    group_models = [ResourceGroup(**g) for g in groups]
    
    request = DiagramRequest(
        title=title,
        resources=resource_models,
        connections=connection_models,
        groups=group_models,
        workspace_dir=workspace_dir,
        filename=filename,
        open_in_vscode=open_in_vscode,
        show_legend=show_legend,
        use_infinite_canvas=use_infinite_canvas,
    )
    
    return await generate_drawio_diagram(request)


@mcp.tool(name='list_azure_shapes')
async def mcp_list_azure_shapes(
    category_filter: Optional[str] = Field(
        None,
        description='Filter by category: compute, network, storage, database, web, security, identity, integration, ai, analytics, devops, management, iot, general'
    ),
) -> ShapesResponse:
    """List all available Azure resource shapes for diagrams.
    
    Returns shapes organized by category with their resource_type identifiers
    that you can use in the generate_diagram tool.
    """
    all_shapes = list_all_shapes()
    
    if category_filter:
        category_filter = category_filter.lower()
        if category_filter in all_shapes:
            filtered = {category_filter: all_shapes[category_filter]}
        else:
            filtered = {}
    else:
        filtered = all_shapes
    
    # Convert to ShapeInfo format
    result: dict = {}
    total = 0
    
    for category, shapes in filtered.items():
        result[category] = []
        for shape in shapes:
            _, _, style = get_shape_info(shape['resource_type'])
            result[category].append(ShapeInfo(
                resource_type=shape['resource_type'],
                display_name=shape['display_name'],
                category=category,
                style=style,
            ))
            total += 1
    
    return ShapesResponse(shapes=result, total_count=total)


@mcp.tool(name='get_diagram_examples')
async def mcp_get_diagram_examples(
    diagram_type: str = Field(
        'all',
        description='Type of example: azure, network, compute, data, integration, security, or all'
    ),
) -> ExampleResponse:
    """Get example diagram specifications to use as templates.
    
    Returns JSON structures that can be used with the generate_diagram tool.
    """
    examples = {}
    
    # Basic Azure Architecture
    if diagram_type in ['azure', 'all']:
        examples['azure_basic'] = {
            'title': 'Basic Azure Web Architecture',
            'resources': [
                {'id': 'user', 'resource_type': 'User', 'name': 'Users', 'rationale': 'End users accessing the application'},
                {'id': 'frontdoor', 'resource_type': 'FrontDoor', 'name': 'Azure Front Door', 'rationale': 'Global load balancer and CDN'},
                {'id': 'webapp', 'resource_type': 'AppService', 'name': 'Web App', 'rationale': 'Web application hosting'},
                {'id': 'sql', 'resource_type': 'SQLDatabase', 'name': 'Azure SQL', 'rationale': 'Relational data storage'},
                {'id': 'storage', 'resource_type': 'StorageAccount', 'name': 'Storage', 'rationale': 'Blob and file storage'},
            ],
            'connections': [
                {'source': 'user', 'target': 'frontdoor'},
                {'source': 'frontdoor', 'target': 'webapp'},
                {'source': 'webapp', 'target': 'sql'},
                {'source': 'webapp', 'target': 'storage'},
            ],
        }
    
    # Network Architecture
    if diagram_type in ['network', 'all']:
        examples['network_hub_spoke'] = {
            'title': 'Hub-Spoke Network Architecture',
            'resources': [
                {'id': 'hub_vnet', 'resource_type': 'VNet', 'name': 'Hub VNet', 'group': 'hub', 'rationale': 'Central hub for shared services'},
                {'id': 'firewall', 'resource_type': 'Firewall', 'name': 'Azure Firewall', 'group': 'hub', 'rationale': 'Centralized network security'},
                {'id': 'bastion', 'resource_type': 'Bastion', 'name': 'Bastion', 'group': 'hub', 'rationale': 'Secure VM access without public IPs'},
                {'id': 'spoke1_vnet', 'resource_type': 'VNet', 'name': 'Spoke 1 VNet', 'group': 'spoke1', 'rationale': 'Isolated workload network'},
                {'id': 'spoke1_vm', 'resource_type': 'VM', 'name': 'Web Server', 'group': 'spoke1', 'rationale': 'Web application hosting'},
                {'id': 'spoke2_vnet', 'resource_type': 'VNet', 'name': 'Spoke 2 VNet', 'group': 'spoke2', 'rationale': 'Container workload network'},
                {'id': 'spoke2_aks', 'resource_type': 'AKS', 'name': 'AKS Cluster', 'group': 'spoke2', 'rationale': 'Kubernetes container orchestration'},
            ],
            'connections': [
                {'source': 'hub_vnet', 'target': 'spoke1_vnet', 'label': 'Peering'},
                {'source': 'hub_vnet', 'target': 'spoke2_vnet', 'label': 'Peering'},
                {'source': 'firewall', 'target': 'spoke1_vm'},
                {'source': 'firewall', 'target': 'spoke2_aks'},
            ],
            'groups': [
                {'id': 'hub', 'name': 'Hub Network', 'color': '#FFF3E0'},
                {'id': 'spoke1', 'name': 'Spoke 1 - Web', 'color': '#E3F2FD'},
                {'id': 'spoke2', 'name': 'Spoke 2 - AKS', 'color': '#E8F5E9'},
            ],
        }
    
    # Compute Architecture
    if diagram_type in ['compute', 'all']:
        examples['compute_aks'] = {
            'title': 'AKS with Application Gateway',
            'resources': [
                {'id': 'agw', 'resource_type': 'ApplicationGateway', 'name': 'App Gateway', 'rationale': 'Layer 7 load balancer with WAF'},
                {'id': 'aks', 'resource_type': 'AKS', 'name': 'AKS Cluster', 'rationale': 'Kubernetes container orchestration'},
                {'id': 'acr', 'resource_type': 'ACR', 'name': 'Container Registry', 'rationale': 'Private container image storage'},
                {'id': 'kv', 'resource_type': 'KeyVault', 'name': 'Key Vault', 'rationale': 'Secrets and certificate management'},
                {'id': 'sql', 'resource_type': 'SQLDatabase', 'name': 'Azure SQL', 'rationale': 'Relational data persistence'},
            ],
            'connections': [
                {'source': 'agw', 'target': 'aks'},
                {'source': 'aks', 'target': 'acr', 'label': 'Pull images'},
                {'source': 'aks', 'target': 'kv', 'label': 'Secrets'},
                {'source': 'aks', 'target': 'sql', 'label': 'Data'},
            ],
        }
    
    # Data Architecture
    if diagram_type in ['data', 'all']:
        examples['data_pipeline'] = {
            'title': 'Azure Data Pipeline',
            'resources': [
                {'id': 'eventhub', 'resource_type': 'EventHub', 'name': 'Event Hubs', 'rationale': 'Real-time event ingestion'},
                {'id': 'stream', 'resource_type': 'StreamAnalytics', 'name': 'Stream Analytics', 'rationale': 'Real-time stream processing'},
                {'id': 'datalake', 'resource_type': 'DataLake', 'name': 'Data Lake', 'rationale': 'Raw data storage'},
                {'id': 'adf', 'resource_type': 'DataFactory', 'name': 'Data Factory', 'rationale': 'ETL orchestration'},
                {'id': 'synapse', 'resource_type': 'Synapse', 'name': 'Synapse Analytics', 'rationale': 'Data warehousing and analytics'},
                {'id': 'powerbi', 'resource_type': 'PowerBI', 'name': 'Power BI', 'rationale': 'Business intelligence reporting'},
            ],
            'connections': [
                {'source': 'eventhub', 'target': 'stream'},
                {'source': 'stream', 'target': 'datalake'},
                {'source': 'datalake', 'target': 'adf'},
                {'source': 'adf', 'target': 'synapse'},
                {'source': 'synapse', 'target': 'powerbi'},
            ],
        }
    
    # Integration Architecture  
    if diagram_type in ['integration', 'all']:
        examples['integration_serverless'] = {
            'title': 'Serverless Integration',
            'resources': [
                {'id': 'apim', 'resource_type': 'APIM', 'name': 'API Management', 'rationale': 'API gateway and management'},
                {'id': 'func1', 'resource_type': 'FunctionApp', 'name': 'Order Function', 'rationale': 'Order processing logic'},
                {'id': 'func2', 'resource_type': 'FunctionApp', 'name': 'Notify Function', 'rationale': 'Notification handling'},
                {'id': 'servicebus', 'resource_type': 'ServiceBus', 'name': 'Service Bus', 'rationale': 'Async message queuing'},
                {'id': 'logic', 'resource_type': 'LogicApp', 'name': 'Workflow', 'rationale': 'Business process automation'},
                {'id': 'cosmos', 'resource_type': 'CosmosDB', 'name': 'Cosmos DB', 'rationale': 'NoSQL data persistence'},
            ],
            'connections': [
                {'source': 'apim', 'target': 'func1'},
                {'source': 'func1', 'target': 'servicebus'},
                {'source': 'servicebus', 'target': 'func2'},
                {'source': 'func2', 'target': 'logic'},
                {'source': 'func1', 'target': 'cosmos'},
            ],
        }
    
    # Security Architecture
    if diagram_type in ['security', 'all']:
        examples['security_zero_trust'] = {
            'title': 'Zero Trust Architecture',
            'resources': [
                {'id': 'user', 'resource_type': 'User', 'name': 'Users', 'rationale': 'End users accessing applications'},
                {'id': 'aad', 'resource_type': 'EntraID', 'name': 'Entra ID', 'rationale': 'Identity and access management'},
                {'id': 'appgw', 'resource_type': 'ApplicationGateway', 'name': 'App Gateway + WAF', 'rationale': 'Web application firewall protection'},
                {'id': 'pe', 'resource_type': 'PrivateEndpoint', 'name': 'Private Endpoints', 'rationale': 'Private network connectivity'},
                {'id': 'kv', 'resource_type': 'KeyVault', 'name': 'Key Vault', 'rationale': 'Secrets management'},
                {'id': 'app', 'resource_type': 'AppService', 'name': 'App Service', 'rationale': 'Application hosting'},
                {'id': 'sentinel', 'resource_type': 'Sentinel', 'name': 'Microsoft Sentinel', 'rationale': 'SIEM and security monitoring'},
            ],
            'connections': [
                {'source': 'user', 'target': 'aad', 'label': 'Authenticate'},
                {'source': 'aad', 'target': 'appgw'},
                {'source': 'appgw', 'target': 'app'},
                {'source': 'app', 'target': 'pe'},
                {'source': 'app', 'target': 'kv'},
                {'source': 'app', 'target': 'sentinel', 'label': 'Logs'},
            ],
        }
    
    return ExampleResponse(examples=examples)


class ScanResult(BaseModel):
    """Result from scanning a workspace for Azure resources."""
    resources_found: int
    connections_inferred: int
    resources: List[Dict]
    connections: List[Dict]
    file_types_scanned: List[str]
    message: str


@mcp.tool(name='scan_workspace')
async def mcp_scan_workspace(
    workspace_dir: str = Field(
        ...,
        description='Path to the workspace directory to scan for Azure resources'
    ),
    generate_diagram: bool = Field(
        True,
        description='Automatically generate a diagram from discovered resources'
    ),
    filename: Optional[str] = Field(
        None,
        description='Output filename for the generated diagram (without extension)'
    ),
    open_in_vscode: bool = Field(
        False,
        description='Open the generated diagram in VS Code'
    ),
) -> dict:
    """Scan a workspace for Azure resources and optionally generate a diagram.
    
    Scans for:
    - Bicep files (*.bicep)
    - Terraform files (*.tf) 
    - ARM templates (*.json with ARM schema)
    - Azure SDK usage in code (*.cs, *.py, *.js, *.ts)
    
    Automatically infers connections between resources based on common patterns.
    """
    # Scan the workspace
    resources, connections = await scan_workspace(workspace_dir)
    
    # Build result
    result = {
        'resources_found': len(resources),
        'connections_inferred': len(connections),
        'resources': [
            {
                'id': r.id,
                'resource_type': r.resource_type,
                'name': r.name,
                'source_file': r.source_file,
                'line_number': r.line_number,
                'rationale': r.rationale,
            }
            for r in resources
        ],
        'connections': [
            {'source': c[0], 'target': c[1], 'label': c[2]}
            for c in connections
        ],
        'file_types_scanned': ['*.bicep', '*.tf', '*.json (ARM)', '*.cs', '*.py', '*.js', '*.ts'],
    }
    
    if len(resources) == 0:
        result['message'] = (
            'No Azure resources found. Make sure the workspace contains '
            'Bicep, Terraform, ARM templates, or code using Azure SDKs.'
        )
        return result
    
    # Generate diagram if requested
    if generate_diagram:
        # Convert discovered resources to AzureResource models
        resource_models = [
            AzureResource(
                id=r.id,
                resource_type=r.resource_type,
                name=r.name,
                rationale=r.rationale,
            )
            for r in resources
        ]
        
        connection_models = [
            Connection(source=c[0], target=c[1], label=c[2])
            for c in connections
        ]
        
        request = DiagramRequest(
            title='Architecture (Auto-Generated)',
            resources=resource_models,
            connections=connection_models,
            groups=[],
            workspace_dir=workspace_dir,
            filename=filename or 'architecture_scan',
            open_in_vscode=open_in_vscode,
            show_legend=True,
        )
        
        diagram_result = await generate_drawio_diagram(request)
        
        result['diagram'] = {
            'status': diagram_result.status,
            'path': diagram_result.path,
            'message': diagram_result.message,
        }
        result['message'] = (
            f"Found {len(resources)} Azure resources and inferred {len(connections)} connections. "
            f"Diagram generated at: {diagram_result.path}"
        )
    else:
        result['message'] = (
            f"Found {len(resources)} Azure resources and inferred {len(connections)} connections. "
            f"Use generate_diagram=True to create a diagram."
        )
    
    return result


def main():
    """Main entry point for the MCP server."""
    print("Azure Draw.io MCP server is running.")
    mcp.run()


if __name__ == "__main__":
    main()
