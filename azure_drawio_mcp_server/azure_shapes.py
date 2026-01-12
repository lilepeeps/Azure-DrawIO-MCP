# Copyright (c) 2026. Inspired by dminkovski/azure-diagram-mcp
"""Azure shape definitions and style mappings for Draw.io diagrams.

This module defines Azure resource shapes using Draw.io's built-in Azure2 icon library.
The icons are SVG-based and render properly in Draw.io and VS Code Draw.io extension.
"""

from typing import Dict, Optional, Tuple

# Azure brand colors (for fallback styling)
AZURE_COLORS = {
    'primary': '#0078D4',      # Azure Blue
    'compute': '#0078D4',      # Blue
    'network': '#59B4D9',      # Light Blue
    'storage': '#00A4EF',      # Sky Blue
    'database': '#F25022',     # Orange/Red
    'web': '#7FBA00',          # Green
    'security': '#FFB900',     # Yellow/Gold
    'identity': '#737373',     # Gray
    'integration': '#00BCF2',  # Cyan
    'devops': '#5C2D91',       # Purple
    'ai': '#68217A',           # Magenta
    'analytics': '#E81123',    # Red
    'iot': '#00B294',          # Teal
    'management': '#0072C6',   # Dark Blue
    'general': '#32CD32',      # Lime Green
    'containers': '#326CE5',   # Kubernetes Blue
}

# Default dimensions for shapes
DEFAULT_WIDTH = 90
DEFAULT_HEIGHT = 90
ICON_SIZE = 68

# Base style for Draw.io Azure2 icons (SVG-based)
# This uses the built-in Azure icon library from Draw.io
AZURE_ICON_BASE_STYLE = (
    "image;aspect=fixed;html=1;points=[];align=center;fontSize=11;"
    "verticalLabelPosition=bottom;verticalAlign=top;labelBackgroundColor=#ffffff;"
)

# Style for general icons (users, clients, etc.) using mxgraph library
GENERAL_ICON_BASE_STYLE = (
    "shape=image;html=1;verticalAlign=top;verticalLabelPosition=bottom;"
    "labelBackgroundColor=#ffffff;fontSize=11;align=center;"
)

# No longer using mxgraph - all icons use Azure2 SVG library which renders properly

# Fallback style for shapes without specific icons
FALLBACK_STYLE = (
    "rounded=1;whiteSpace=wrap;html=1;arcSize=10;"
    "strokeWidth=2;shadow=1;glass=0;"
    "fontColor=#FFFFFF;fontSize=11;fontStyle=1;"
    "verticalAlign=middle;align=center;"
)


def get_azure_icon_style(image_path: str) -> str:
    """Generate Draw.io style string for an Azure icon using the Azure2 library."""
    return f"{AZURE_ICON_BASE_STYLE}image=img/lib/azure2/{image_path};"


def get_general_icon_style(image_path: str) -> str:
    """Generate Draw.io style string for general icons (users, devices, etc.)."""
    return f"{GENERAL_ICON_BASE_STYLE}image={image_path};"


def get_fallback_style(category: str, fill_color: Optional[str] = None) -> str:
    """Generate fallback style for resources without specific icons."""
    color = fill_color or AZURE_COLORS.get(category, AZURE_COLORS['primary'])
    return f"{FALLBACK_STYLE}fillColor={color};strokeColor=#003366;"


def get_group_style(color: Optional[str] = None) -> str:
    """Generate Draw.io style string for a resource group (cluster/container)."""
    fill = color or '#E6F3FF'
    return (
        # Visual styling for swimlane-like container
        "swimlane;whiteSpace=wrap;html=1;"
        f"fillColor={fill};fillOpacity=50;strokeColor=#0078D4;strokeWidth=2;"
        "rounded=1;startSize=30;horizontal=1;"
        "fontSize=12;fontStyle=1;fontColor=#0078D4;"
        "shadow=0;glass=0;"
    )


def get_edge_style(style: str = 'solid') -> str:
    """Generate Draw.io style string for an edge/connection."""
    base = (
        "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;"
        "jettySize=auto;html=1;strokeWidth=2;strokeColor=#0078D4;"
        "endArrow=blockThin;endFill=1;"
    )
    if style == 'dashed':
        base += "dashed=1;dashPattern=8 8;"
    elif style == 'dotted':
        base += "dashed=1;dashPattern=2 2;"
    return base


# Azure resource type to shape mapping
# Maps resource_type strings to (display_name, category, azure2_icon_path or None for fallback)
# Icon paths reference Draw.io's built-in Azure2 library: img/lib/azure2/<path>
AZURE_SHAPES: Dict[str, Tuple[str, str, Optional[str]]] = {
    # ========== Compute ==========
    'VM': ('Virtual Machine', 'compute', 'compute/Virtual_Machine.svg'),
    'VirtualMachine': ('Virtual Machine', 'compute', 'compute/Virtual_Machine.svg'),
    'VMSS': ('VM Scale Set', 'compute', 'compute/VM_Scale_Sets.svg'),
    'VMScaleSet': ('VM Scale Set', 'compute', 'compute/VM_Scale_Sets.svg'),
    'AppService': ('App Service', 'compute', 'app_services/App_Services.svg'),
    'WebApp': ('Web App', 'compute', 'app_services/App_Services.svg'),
    'FunctionApp': ('Function App', 'compute', 'compute/Function_Apps.svg'),
    'Function': ('Azure Function', 'compute', 'compute/Function_Apps.svg'),
    'AKS': ('AKS Cluster', 'containers', 'containers/Kubernetes_Services.svg'),
    'Kubernetes': ('Kubernetes Service', 'containers', 'containers/Kubernetes_Services.svg'),
    'ContainerInstances': ('Container Instances', 'containers', 'containers/Container_Instances.svg'),
    'ContainerRegistry': ('Container Registry', 'containers', 'containers/Container_Registries.svg'),
    'ACR': ('Container Registry', 'containers', 'containers/Container_Registries.svg'),
    'BatchAccount': ('Batch Account', 'compute', 'compute/Batch_Accounts.svg'),
    'CloudServices': ('Cloud Services', 'compute', 'compute/Cloud_Services_Classic.svg'),
    'ServiceFabric': ('Service Fabric', 'compute', 'compute/Service_Fabric_Clusters.svg'),
    'ContainerApps': ('Container Apps', 'containers', 'containers/Container_Apps.svg'),
    
    # ========== Network (some need mxgraph fallback) ==========
    'VNet': ('Virtual Network', 'network', 'networking/Virtual_Networks.svg'),
    'VirtualNetwork': ('Virtual Network', 'network', 'networking/Virtual_Networks.svg'),
    'Subnet': ('Subnet', 'network', 'networking/Subnet.svg'),
    'LoadBalancer': ('Load Balancer', 'network', 'networking/Load_Balancers.svg'),
    'ApplicationGateway': ('Application Gateway', 'network', 'networking/Application_Gateways.svg'),
    'AppGateway': ('Application Gateway', 'network', 'networking/Application_Gateways.svg'),
    'FrontDoor': ('Front Door', 'network', 'networking/Front_Doors.svg'),
    'TrafficManager': ('Traffic Manager', 'network', 'networking/Traffic_Manager_Profiles.svg'),
    'CDN': ('CDN Profile', 'network', 'networking/CDN_Profiles.svg'),
    'DNS': ('Azure DNS', 'network', 'networking/DNS_Zones.svg'),
    'PrivateLink': ('Private Link', 'network', 'networking/Private_Link.svg'),
    'PrivateEndpoint': ('Private Endpoint', 'network', 'networking/Private_Endpoint.svg'),
    'Firewall': ('Azure Firewall', 'network', 'networking/Firewalls.svg'),
    'WAF': ('Web App Firewall', 'network', 'networking/Web_Application_Firewall_Policies_WAF.svg'),
    'VPNGateway': ('VPN Gateway', 'network', 'networking/Virtual_Network_Gateways.svg'),
    'ExpressRoute': ('ExpressRoute', 'network', 'networking/ExpressRoute_Circuits.svg'),
    'Bastion': ('Azure Bastion', 'network', 'networking/Bastions.svg'),
    'NSG': ('Network Security Group', 'network', 'networking/Network_Security_Groups.svg'),
    'NetworkSecurityGroup': ('Network Security Group', 'network', 'networking/Network_Security_Groups.svg'),
    'PublicIP': ('Public IP', 'network', 'networking/Public_IP_Addresses.svg'),
    'NIC': ('Network Interface', 'network', 'networking/Network_Interfaces.svg'),
    
    # ========== Storage ==========
    'StorageAccount': ('Storage Account', 'storage', 'storage/Storage_Accounts.svg'),
    'BlobStorage': ('Blob Storage', 'storage', 'storage/Blob_Block.svg'),
    'FileStorage': ('File Storage', 'storage', 'storage/Storage_Azure_Files.svg'),
    'QueueStorage': ('Queue Storage', 'storage', 'storage/Queue_Storage.svg'),
    'TableStorage': ('Table Storage', 'storage', 'storage/Table_Storage.svg'),
    'DataLake': ('Data Lake Storage', 'storage', 'storage/Data_Lake_Storage_Gen1.svg'),
    'ManagedDisk': ('Managed Disk', 'storage', 'compute/Disks.svg'),
    'Disk': ('Disk', 'storage', 'compute/Disks.svg'),
    'NetAppFiles': ('NetApp Files', 'storage', 'storage/Azure_NetApp_Files.svg'),
    
    # ========== Database ==========
    'SQLDatabase': ('SQL Database', 'database', 'databases/SQL_Database.svg'),
    'SQLDB': ('SQL Database', 'database', 'databases/SQL_Database.svg'),
    'SQLServer': ('SQL Server', 'database', 'databases/SQL_Server.svg'),
    'CosmosDB': ('Cosmos DB', 'database', 'databases/Azure_Cosmos_DB.svg'),
    'MySQL': ('MySQL', 'database', 'databases/Azure_Database_MySQL_Server.svg'),
    'PostgreSQL': ('PostgreSQL', 'database', 'databases/Azure_Database_PostgreSQL_Server.svg'),
    'MariaDB': ('MariaDB', 'database', 'databases/Azure_Database_MariaDB_Server.svg'),
    'Redis': ('Redis Cache', 'database', 'databases/Cache_Redis.svg'),
    'RedisCache': ('Redis Cache', 'database', 'databases/Cache_Redis.svg'),
    'SQLManagedInstance': ('SQL Managed Instance', 'database', 'databases/SQL_Managed_Instance.svg'),
    'Synapse': ('Synapse Analytics', 'database', 'databases/Azure_Synapse_Analytics.svg'),
    
    # ========== Web ==========
    'APIManagement': ('API Management', 'web', 'integration/API_Management_Services.svg'),
    'APIM': ('API Management', 'web', 'integration/API_Management_Services.svg'),
    'SignalR': ('SignalR Service', 'web', 'app_services/SignalR.svg'),
    'StaticWebApp': ('Static Web App', 'web', 'preview/Static_Apps.svg'),
    'AppServicePlan': ('App Service Plan', 'web', 'app_services/App_Service_Plans.svg'),
    
    # ========== Security & Identity ==========
    'KeyVault': ('Key Vault', 'security', 'security/Key_Vaults.svg'),
    'AAD': ('Azure AD', 'identity', 'identity/Azure_AD.svg'),
    'AzureAD': ('Azure AD', 'identity', 'identity/Azure_AD.svg'),
    'EntraID': ('Entra ID', 'identity', 'identity/Entra_ID.svg'),
    'ManagedIdentity': ('Managed Identity', 'identity', 'identity/Managed_Identities.svg'),
    'SecurityCenter': ('Security Center', 'security', 'security/Security_Center.svg'),
    'Sentinel': ('Sentinel', 'security', 'security/Microsoft_Sentinel.svg'),
    'DDoSProtection': ('DDoS Protection', 'security', 'networking/DDoS_Protection_Plans.svg'),
    'Defender': ('Microsoft Defender', 'security', 'security/Microsoft_Defender_for_Cloud.svg'),
    
    # ========== Integration ==========
    'ServiceBus': ('Service Bus', 'integration', 'integration/Service_Bus.svg'),
    'EventHub': ('Event Hubs', 'integration', 'integration/Event_Hubs.svg'),
    'EventGrid': ('Event Grid', 'integration', 'integration/Event_Grid_Topics.svg'),
    'LogicApp': ('Logic App', 'integration', 'integration/Logic_Apps.svg'),
    'DataFactory': ('Data Factory', 'integration', 'databases/Data_Factory.svg'),
    'APIConnections': ('API Connections', 'integration', 'devops/API_Connections.svg'),
    
    # ========== AI & ML ==========
    'CognitiveServices': ('Cognitive Services', 'ai', 'ai_machine_learning/Cognitive_Services.svg'),
    'MachineLearning': ('Machine Learning', 'ai', 'ai_machine_learning/Machine_Learning.svg'),
    'AzureML': ('Azure ML', 'ai', 'ai_machine_learning/Machine_Learning.svg'),
    'OpenAI': ('Azure OpenAI', 'ai', 'ai_machine_learning/Azure_OpenAI.svg'),
    'AzureOpenAI': ('Azure OpenAI', 'ai', 'ai_machine_learning/Azure_OpenAI.svg'),
    'BotService': ('Bot Service', 'ai', 'ai_machine_learning/Bot_Services.svg'),
    'SearchService': ('AI Search', 'ai', 'ai_machine_learning/Cognitive_Search.svg'),
    'AISearch': ('AI Search', 'ai', 'ai_machine_learning/Cognitive_Search.svg'),
    
    # ========== Analytics ==========
    'StreamAnalytics': ('Stream Analytics', 'analytics', 'analytics/Stream_Analytics_Jobs.svg'),
    'HDInsight': ('HDInsight', 'analytics', 'analytics/HD_Insight_Clusters.svg'),
    'Databricks': ('Databricks', 'analytics', 'analytics/Azure_Databricks.svg'),
    'PowerBI': ('Power BI', 'analytics', 'analytics/Power_BI_Embedded.svg'),
    'AnalysisServices': ('Analysis Services', 'analytics', 'analytics/Analysis_Services.svg'),
    
    # ========== DevOps & Management ==========
    'DevOps': ('Azure DevOps', 'devops', 'devops/Azure_DevOps.svg'),
    'Monitor': ('Azure Monitor', 'management', 'management_governance/Monitor.svg'),
    'LogAnalytics': ('Log Analytics', 'management', 'management_governance/Log_Analytics_Workspaces.svg'),
    'AppInsights': ('Application Insights', 'management', 'management_governance/Application_Insights.svg'),
    'ApplicationInsights': ('Application Insights', 'management', 'management_governance/Application_Insights.svg'),
    'Automation': ('Automation', 'management', 'management_governance/Automation_Accounts.svg'),
    'ResourceGroup': ('Resource Group', 'management', 'management_governance/Resource_Groups.svg'),
    'Subscription': ('Subscription', 'management', 'management_governance/Subscriptions.svg'),
    'ManagementGroup': ('Management Group', 'management', 'management_governance/Management_Groups.svg'),
    'Policy': ('Azure Policy', 'management', 'management_governance/Policy.svg'),
    'Blueprint': ('Blueprint', 'management', 'management_governance/Blueprints.svg'),
    
    # ========== IoT ==========
    'IoTHub': ('IoT Hub', 'iot', 'iot/IoT_Hub.svg'),
    'IoTCentral': ('IoT Central', 'iot', 'iot/IoT_Central_Applications.svg'),
    'DigitalTwins': ('Digital Twins', 'iot', 'iot/Digital_Twins.svg'),
    'TimeSeriesInsights': ('Time Series Insights', 'iot', 'iot/Time_Series_Insights_Environments.svg'),
    
    # ========== General / Users (using Azure2 identity and general icons) ==========
    'User': ('User', 'identity', 'identity/Users.svg'),
    'Users': ('Users', 'identity', 'identity/Groups.svg'),
    'Client': ('Client', 'identity', 'identity/External_Identities.svg'),
    'Browser': ('Browser', 'general', 'general/Browser.svg'),
    'Mobile': ('Mobile App', 'general', 'general/Mobile.svg'),
    'OnPremise': ('On-Premises', 'general', 'networking/On_Premises_Data_Gateways.svg'),
    'OnPrem': ('On-Premises', 'general', 'networking/On_Premises_Data_Gateways.svg'),
    'Internet': ('Internet', 'general', 'general/Globe_Success.svg'),
    'Cloud': ('Cloud', 'general', 'azure_ecosystem/Azure.svg'),
}


def get_shape_info(resource_type: str) -> Tuple[str, str, str]:
    """
    Get shape information for a resource type.
    
    Returns: (display_name, category, style_string)
    
    Uses Draw.io's built-in Azure2 SVG icons for all resources.
    """
    if resource_type in AZURE_SHAPES:
        display_name, category, icon_path = AZURE_SHAPES[resource_type]
        
        if icon_path:
            # Use Draw.io Azure2 icon library
            style = get_azure_icon_style(icon_path)
        else:
            # Fallback to colored rectangle
            style = get_fallback_style(category)
        
        return (display_name, category, style)
    else:
        # Unknown resource type - use generic fallback style
        return (resource_type, 'general', get_fallback_style('general'))


def list_all_shapes() -> Dict[str, list]:
    """List all available shapes organized by category."""
    categories: Dict[str, list] = {}
    
    for resource_type, (display_name, category, _) in AZURE_SHAPES.items():
        if category not in categories:
            categories[category] = []
        categories[category].append({
            'resource_type': resource_type,
            'display_name': display_name,
        })
    
    return categories
