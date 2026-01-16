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

# Default dimensions for shapes - compact for A4/PowerPoint diagrams
DEFAULT_WIDTH = 60
DEFAULT_HEIGHT = 50
ICON_SIZE = 40  # Small icons for compact layouts

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

# Fallback style for shapes without specific icons - subtle gray box
FALLBACK_STYLE = (
    "rounded=1;whiteSpace=wrap;html=1;arcSize=8;"
    "strokeWidth=1;shadow=0;glass=0;"
    "fontColor=#333333;fontSize=10;fontStyle=0;"
    "verticalAlign=middle;align=center;"
    "fillColor=#F5F5F5;strokeColor=#CCCCCC;"
)


def get_azure_icon_style(image_path: str) -> str:
    """Generate Draw.io style string for an Azure icon using the Azure2 library."""
    return f"{AZURE_ICON_BASE_STYLE}image=img/lib/azure2/{image_path};"


def get_general_icon_style(image_path: str) -> str:
    """Generate Draw.io style string for general icons (users, devices, etc.)."""
    return f"{GENERAL_ICON_BASE_STYLE}image={image_path};"


def get_fallback_style(category: str, fill_color: Optional[str] = None) -> str:
    """Generate fallback style for resources without specific icons."""
    # Use the pre-defined fallback style (already has fill and stroke)
    return FALLBACK_STYLE


def get_group_style(color: Optional[str] = None, style: str = 'swimlane') -> str:
    """Generate Draw.io style string for a resource group (cluster/container).
    
    Args:
        color: Background fill color (hex)
        style: 'swimlane' for titled container, 'box' for simple compact rectangle
    """
    fill = color or '#E6E6E6'
    
    if style == 'box':
        # Compact box style for professional diagrams - solid gray fill, no stroke
        # Label positioned at top, vertically aligned to top
        return (
            "rounded=0;whiteSpace=wrap;html=1;"
            f"fillColor={fill};strokeColor=none;"
            "verticalAlign=top;align=center;"
            "fontSize=10;fontStyle=1;fontColor=#333333;"
            "spacingTop=5;"
        )
    elif style == 'dashed':
        # Dashed outline for resource group boundaries
        return (
            "rounded=0;whiteSpace=wrap;html=1;dashed=1;"
            "fillColor=none;strokeColor=#0078D4;strokeWidth=1;"
            "verticalAlign=top;align=center;"
            "fontSize=10;fontStyle=1;fontColor=#0078D4;"
        )
    else:
        # Swimlane style with title bar (default)
        return (
            "swimlane;whiteSpace=wrap;html=1;"
            f"fillColor={fill};fillOpacity=50;strokeColor=#0078D4;strokeWidth=2;"
            "rounded=1;startSize=30;horizontal=1;"
            "fontSize=12;fontStyle=1;fontColor=#0078D4;"
            "shadow=0;glass=0;"
        )


def get_edge_style(style: str = 'solid', filled_arrow: bool = False) -> str:
    """Generate Draw.io style string for an edge/connection.
    
    Args:
        style: Line style - 'solid', 'dashed', or 'dotted'
        filled_arrow: If True, use filled arrowhead; if False, use hollow (outline) arrowhead
    """
    # Use hollow arrowhead (endFill=0) by default for cleaner professional look
    end_fill = "1" if filled_arrow else "0"
    base = (
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;"
        f"jettySize=auto;html=1;strokeWidth=2;strokeColor=#6c8ebf;"
        f"endArrow=blockThin;endFill={end_fill};fillColor=#dae8fc;"
        "labelBackgroundColor=none;"
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
    'AVSVM': ('AVS VM', 'compute', 'other/AVS_VM.svg'),
    'ApplicationGroup': ('Application Group', 'compute', 'compute/Application_Group.svg'),
    'AutomanagedVM': ('Automanaged VM', 'compute', 'compute/Automanaged_VM.svg'),
    'AvailabilitySet': ('Availability Sets', 'compute', 'compute/Availability_Sets.svg'),
    'AzureComputeGallery': ('Azure Compute Galleries', 'compute', 'compute/Azure_Compute_Galleries.svg'),
    'AzureSQLVM': ('Azure SQL VM', 'compute', 'databases/Azure_SQL_VM.svg'),
    'AzureSpringCloud': ('Azure Spring Cloud', 'compute', 'compute/Azure_Spring_Cloud.svg'),
    'BatchAccount': ('Batch Accounts', 'compute', 'compute/Batch_Accounts.svg'),
    'CloudServicesClassic': ('Cloud Services Classic', 'compute', 'compute/Cloud_Services_Classic.svg'),
    'ContainerInstance': ('Container Instances', 'compute', 'compute/Container_Instances.svg'),
    'ContainerServicesDeprecated': ('Container Services Deprecated', 'compute', 'compute/Container_Services_Deprecated.svg'),
    'Disk': ('Disks', 'compute', 'compute/Disks.svg'),
    'DiskEncryptionSet': ('Disk Encryption Sets', 'compute', 'compute/Disk_Encryption_Sets.svg'),
    'DisksClassic': ('Disks Classic', 'compute', 'compute/Disks_Classic.svg'),
    'DisksSnapshot': ('Disks Snapshots', 'compute', 'compute/Disks_Snapshots.svg'),
    'FunctionApp': ('Function Apps', 'compute', 'compute/Function_Apps.svg'),
    'FunctionApps': ('Function Apps', 'compute', 'compute/Function_Apps.svg'),  # Alias
    'Host': ('Hosts', 'compute', 'compute/Hosts.svg'),
    'HostGroup': ('Host Groups', 'compute', 'compute/Host_Groups.svg'),
    'HostPool': ('Host Pools', 'compute', 'compute/Host_Pools.svg'),
    'Image': ('Images', 'compute', 'compute/Images.svg'),
    'ImageDefinition': ('Image Definitions', 'compute', 'compute/Image_Definitions.svg'),
    'ImageTemplate': ('Image Templates', 'compute', 'compute/Image_Templates.svg'),
    'ImageVersion': ('Image Versions', 'compute', 'compute/Image_Versions.svg'),
    'KubernetesServices': ('Kubernetes Services', 'compute', 'compute/Kubernetes_Services.svg'),
    'MaintenanceConfiguration': ('Maintenance Configuration', 'compute', 'compute/Maintenance_Configuration.svg'),
    'ManagedServiceFabric': ('Managed Service Fabric', 'compute', 'compute/Managed_Service_Fabric.svg'),
    'MeshApplication': ('Mesh Applications', 'compute', 'compute/Mesh_Applications.svg'),
    'MetricsAdvisor': ('Metrics Advisor', 'compute', 'compute/Metrics_Advisor.svg'),
    'OSImagesClassic': ('OS Images Classic', 'compute', 'compute/OS_Images_Classic.svg'),
    'ProximityPlacementGroup': ('Proximity Placement Groups', 'compute', 'networking/Proximity_Placement_Groups.svg'),
    'RestorePoint': ('Restore Points', 'compute', 'compute/Restore_Points.svg'),
    'RestorePointsCollection': ('Restore Points Collections', 'compute', 'compute/Restore_Points_Collections.svg'),
    'SCVMMManagementServer': ('SCVMM Management Servers', 'compute', 'other/SCVMM_Management_Servers.svg'),
    'ServiceFabricCluster': ('Service Fabric Clusters', 'compute', 'compute/Service_Fabric_Clusters.svg'),
    'SharedImageGallery': ('Shared Image Galleries', 'compute', 'compute/Shared_Image_Galleries.svg'),
    'SpotVM': ('Spot VM', 'compute', 'networking/Spot_VM.svg'),
    'SpotVMSS': ('Spot VMSS', 'compute', 'networking/Spot_VMSS.svg'),
    'VMApplicationDefinition': ('VM Application Definition', 'compute', 'other/VM_Application_Definition.svg'),
    'VMApplicationVersion': ('VM Application Version', 'compute', 'other/VM_Application_Version.svg'),
    'VMImagesClassic': ('VM Images Classic', 'compute', 'compute/VM_Images_Classic.svg'),
    'VMScaleSet': ('VM Scale Sets', 'compute', 'compute/VM_Scale_Sets.svg'),
    'VirtualMachine': ('Virtual Machine', 'compute', 'compute/Virtual_Machine.svg'),
    'VirtualMachinesClassic': ('Virtual Machines Classic', 'compute', 'compute/Virtual_Machines_Classic.svg'),
    'Workspace': ('Workspaces', 'compute', 'compute/Workspaces.svg'),
    'Workspaces2': ('Workspaces2', 'compute', 'compute/Workspaces2.svg'),

    # ========== Containers ==========
    'AzureRedHatOpenShift': ('Azure Red Hat OpenShift', 'containers', 'containers/Azure_Red_Hat_OpenShift.svg'),
    'ContainerRegistry': ('Container Registries', 'containers', 'containers/Container_Registries.svg'),
    'ContainersBatchAccount': ('Batch Accounts', 'containers', 'containers/Batch_Accounts.svg'),
    'ContainersContainerInstance': ('Container Instances', 'containers', 'containers/Container_Instances.svg'),
    'ContainersKubernetesServices': ('Kubernetes Services', 'containers', 'containers/Kubernetes_Services.svg'),
    'ContainersServiceFabricCluster': ('Service Fabric Clusters', 'containers', 'containers/Service_Fabric_Clusters.svg'),

    # ========== Network ==========
    'ATMMultistack': ('ATM Multistack', 'network', 'networking/ATM_Multistack.svg'),
    'ApplicationGateway': ('Application Gateways', 'network', 'networking/Application_Gateways.svg'),
    'ApplicationGatewayContainer': ('Application Gateway Containers', 'network', 'networking/Application_Gateway_Containers.svg'),
    'AzureCommunicationsGateway': ('Azure Communications Gateway', 'network', 'networking/Azure_Communications_Gateway.svg'),
    'AzureFirewallManager': ('Azure Firewall Manager', 'network', 'networking/Azure_Firewall_Manager.svg'),
    'AzureFirewallPolicy': ('Azure Firewall Policy', 'network', 'networking/Azure_Firewall_Policy.svg'),
    'Bastion': ('Bastions', 'network', 'networking/Bastions.svg'),
    'CDNProfile': ('CDN Profiles', 'network', 'networking/CDN_Profiles.svg'),
    'Connection': ('Connections', 'network', 'networking/Connections.svg'),
    'DDoSProtectionPlan': ('DDoS Protection Plans', 'network', 'networking/DDoS_Protection_Plans.svg'),
    'DNSMultistack': ('DNS Multistack', 'network', 'networking/DNS_Multistack.svg'),
    'DNSPrivateResolver': ('DNS Private Resolver', 'network', 'networking/DNS_Private_Resolver.svg'),
    'DNSSecurityPolicy': ('DNS Security Policy', 'network', 'networking/DNS_Security_Policy.svg'),
    'DNSZone': ('DNS Zones', 'network', 'networking/DNS_Zones.svg'),
    'AzureDns': ('Azure DNS', 'network', 'networking/DNS_Zones.svg'),  # Alias for DNSZone
    'ExpressRouteCircuits': ('ExpressRoute Circuits', 'network', 'networking/ExpressRoute_Circuits.svg'),
    'Firewall': ('Firewalls', 'network', 'networking/Firewalls.svg'),
    'FrontDoor': ('Front Doors', 'network', 'networking/Front_Doors.svg'),
    'IPAddressmanager': ('IP Address manager', 'network', 'networking/IP_Address_manager.svg'),
    'IPGroup': ('IP Groups', 'network', 'networking/IP_Groups.svg'),
    'LoadBalancer': ('Load Balancers', 'network', 'networking/Load_Balancers.svg'),
    'LoadBalancerHub': ('Load Balancer Hub', 'network', 'networking/Load_Balancer_Hub.svg'),
    'LocalNetworkGateway': ('Local Network Gateways', 'network', 'networking/Local_Network_Gateways.svg'),
    'NAT': ('NAT', 'network', 'networking/NAT.svg'),
    'NetworkInterface': ('Network Interfaces', 'network', 'networking/Network_Interfaces.svg'),
    'NetworkSecurityGroup': ('Network Security Groups', 'network', 'networking/Network_Security_Groups.svg'),
    'NetworkWatcher': ('Network Watcher', 'network', 'networking/Network_Watcher.svg'),
    'OnPremisesDataGateway': ('On Premises Data Gateways', 'network', 'networking/On_Premises_Data_Gateways.svg'),
    'PrivateEndpoint': ('Private Endpoint', 'network', 'networking/Private_Endpoint.svg'),
    'PrivateLink': ('Private Link', 'network', 'networking/Private_Link.svg'),
    'PrivateLinkHub': ('Private Link Hub', 'network', 'networking/Private_Link_Hub.svg'),
    'PrivateLinkService': ('Private Link Service', 'network', 'networking/Private_Link_Service.svg'),
    'PublicIPAddress': ('Public IP Addresses', 'network', 'networking/Public_IP_Addresses.svg'),
    'PublicIPAddressesClassic': ('Public IP Addresses Classic', 'network', 'networking/Public_IP_Addresses_Classic.svg'),
    'PublicIPPrefix': ('Public IP Prefixes', 'network', 'networking/Public_IP_Prefixes.svg'),
    'ReservedIPAddressesClassic': ('Reserved IP Addresses Classic', 'network', 'networking/Reserved_IP_Addresses_Classic.svg'),
    'ResourceManagementPrivateLink': ('Resource Management Private Link', 'network', 'networking/Resource_Management_Private_Link.svg'),
    'RouteFilter': ('Route Filters', 'network', 'networking/Route_Filters.svg'),
    'RouteTable': ('Route Tables', 'network', 'networking/Route_Tables.svg'),
    'ServiceEndpointPolicy': ('Service Endpoint Policies', 'network', 'networking/Service_Endpoint_Policies.svg'),
    'Subnet': ('Subnet', 'network', 'networking/Subnet.svg'),
    'TrafficManagerProfile': ('Traffic Manager Profiles', 'network', 'networking/Traffic_Manager_Profiles.svg'),
    'VirtualNetwork': ('Virtual Networks', 'network', 'networking/Virtual_Networks.svg'),
    'VirtualNetworkGateway': ('Virtual Network Gateways', 'network', 'networking/Virtual_Network_Gateways.svg'),
    'VirtualNetworksClassic': ('Virtual Networks Classic', 'network', 'networking/Virtual_Networks_Classic.svg'),
    'VirtualRouter': ('Virtual Router', 'network', 'networking/Virtual_Router.svg'),
    'VirtualWAN': ('Virtual WANs', 'network', 'networking/Virtual_WANs.svg'),
    'VirtualWANHub': ('Virtual WAN Hub', 'network', 'networking/Virtual_WAN_Hub.svg'),
    'WebApplicationFirewallPoliciesWAF': ('Web Application Firewall Policies WAF', 'network', 'networking/Web_Application_Firewall_Policies_WAF.svg'),

    # ========== Storage ==========
    'AzureFileshare': ('Azure Fileshare', 'storage', 'storage/Azure_Fileshare.svg'),
    'AzureHCPCache': ('Azure HCP Cache', 'storage', 'storage/Azure_HCP_Cache.svg'),
    'AzureNetAppFile': ('Azure NetApp Files', 'storage', 'storage/Azure_NetApp_Files.svg'),
    'AzureStackEdge': ('Azure Stack Edge', 'storage', 'storage/Azure_Stack_Edge.svg'),
    'BlobBlock': ('Blob Block', 'storage', 'general/Blob_Block.svg'),
    'BlobPage': ('Blob Page', 'storage', 'general/Blob_Page.svg'),
    'DataBox': ('Data Box', 'storage', 'storage/Data_Box.svg'),
    'DataBoxEdge': ('Data Box Edge', 'storage', 'storage/Data_Box_Edge.svg'),
    'DataLakeStorageGen1': ('Data Lake Storage Gen1', 'storage', 'storage/Data_Lake_Storage_Gen1.svg'),
    'DataShare': ('Data Shares', 'storage', 'storage/Data_Shares.svg'),
    'DataShareInvitation': ('Data Share Invitations', 'storage', 'storage/Data_Share_Invitations.svg'),
    'ImportExportJob': ('Import Export Jobs', 'storage', 'storage/Import_Export_Jobs.svg'),
    'RecoveryServicesVaults': ('Recovery Services Vaults', 'storage', 'storage/Recovery_Services_Vaults.svg'),
    'StorSimpleDataManager': ('StorSimple Data Managers', 'storage', 'storage/StorSimple_Data_Managers.svg'),
    'StorSimpleDeviceManager': ('StorSimple Device Managers', 'storage', 'storage/StorSimple_Device_Managers.svg'),
    'StorageAccount': ('Storage Accounts', 'storage', 'storage/Storage_Accounts.svg'),
    'StorageAccountsClassic': ('Storage Accounts Classic', 'storage', 'storage/Storage_Accounts_Classic.svg'),
    'StorageAzureFiles': ('Storage Azure Files', 'storage', 'general/Storage_Azure_Files.svg'),
    'StorageContainer': ('Storage Container', 'storage', 'general/Storage_Container.svg'),
    'StorageExplorer': ('Storage Explorer', 'storage', 'storage/Storage_Explorer.svg'),
    'StorageQueue': ('Storage Queue', 'storage', 'general/Storage_Queue.svg'),
    'StorageSyncService': ('Storage Sync Services', 'storage', 'storage/Storage_Sync_Services.svg'),

    # ========== Database ==========
    'AzureCosmosDB': ('Azure Cosmos DB', 'database', 'databases/Azure_Cosmos_DB.svg'),
    'AzureDataExplorerCluster': ('Azure Data Explorer Clusters', 'database', 'databases/Azure_Data_Explorer_Clusters.svg'),
    'AzureDatabaseMariaDBServer': ('Azure Database MariaDB Server', 'database', 'databases/Azure_Database_MariaDB_Server.svg'),
    'AzureDatabaseMigrationService': ('Azure Database Migration Services', 'database', 'databases/Azure_Database_Migration_Services.svg'),
    'AzureDatabaseMySQLServer': ('Azure Database MySQL Server', 'database', 'databases/Azure_Database_MySQL_Server.svg'),
    'AzureDatabasePostgreSQLServer': ('Azure Database PostgreSQL Server', 'database', 'databases/Azure_Database_PostgreSQL_Server.svg'),
    'AzureDatabasePostgreSQLServerGroup': ('Azure Database PostgreSQL Server Group', 'database', 'databases/Azure_Database_PostgreSQL_Server_Group.svg'),
    'AzurePurviewAccount': ('Azure Purview Accounts', 'database', 'databases/Azure_Purview_Accounts.svg'),
    'AzureSQL': ('Azure SQL', 'database', 'databases/Azure_SQL.svg'),
    'AzureSQLEdge': ('Azure SQL Edge', 'database', 'databases/Azure_SQL_Edge.svg'),
    'AzureSQLServerStretchDatabase': ('Azure SQL Server Stretch Databases', 'database', 'databases/Azure_SQL_Server_Stretch_Databases.svg'),
    'AzureSynapseAnalytics': ('Azure Synapse Analytics', 'database', 'databases/Azure_Synapse_Analytics.svg'),
    'CacheRedis': ('Cache Redis', 'database', 'databases/Cache_Redis.svg'),
    'DataFactory': ('Data Factory', 'database', 'databases/Data_Factory.svg'),
    'ElasticJobAgent': ('Elastic Job Agents', 'database', 'databases/Elastic_Job_Agents.svg'),
    'InstancePool': ('Instance Pools', 'database', 'databases/Instance_Pools.svg'),
    'ManagedDatabase': ('Managed Database', 'database', 'databases/Managed_Database.svg'),
    'OracleDatabase': ('Oracle Database', 'database', 'databases/Oracle_Database.svg'),
    'SQLDataWarehouse': ('SQL Data Warehouses', 'database', 'databases/SQL_Data_Warehouses.svg'),
    'SQLDatabase': ('SQL Database', 'database', 'databases/SQL_Database.svg'),
    'SQLElasticPool': ('SQL Elastic Pools', 'database', 'databases/SQL_Elastic_Pools.svg'),
    'SQLManagedInstance': ('SQL Managed Instance', 'database', 'databases/SQL_Managed_Instance.svg'),
    'SQLServer': ('SQL Server', 'database', 'databases/SQL_Server.svg'),
    'SQLServerRegistry': ('SQL Server Registries', 'database', 'databases/SQL_Server_Registries.svg'),
    'SSISLiftAndShiftIR': ('SSIS Lift And Shift IR', 'database', 'databases/SSIS_Lift_And_Shift_IR.svg'),
    'VirtualCluster': ('Virtual Clusters', 'database', 'databases/Virtual_Clusters.svg'),

    # ========== Web ==========
    'APICenter': ('API Center', 'web', 'web/API_Center.svg'),
    'APIManagementService': ('API Management Services', 'web', 'app_services/API_Management_Services.svg'),
    'AppService': ('App Services', 'web', 'app_services/App_Services.svg'),
    'AppServices': ('App Services', 'web', 'app_services/App_Services.svg'),  # Alias
    'AppServiceCertificate': ('App Service Certificates', 'web', 'app_services/App_Service_Certificates.svg'),
    'AppServiceDomain': ('App Service Domains', 'web', 'app_services/App_Service_Domains.svg'),
    'AppServiceEnvironment': ('App Service Environments', 'web', 'app_services/App_Service_Environments.svg'),
    'AppServicePlan': ('App Service Plans', 'web', 'app_services/App_Service_Plans.svg'),
    'AppSpace': ('App Space', 'web', 'web/App_Space.svg'),
    'AppservicesCDNProfile': ('CDN Profiles', 'web', 'app_services/CDN_Profiles.svg'),
    'AzureMediaService': ('Azure Media Service', 'web', 'web/Azure_Media_Service.svg'),
    'ComputeAppService': ('App Services', 'web', 'compute/App_Services.svg'),
    'ContainersAppService': ('App Services', 'web', 'containers/App_Services.svg'),
    'NotificationHub': ('Notification Hubs', 'web', 'app_services/Notification_Hubs.svg'),
    'NotificationHubNamespace': ('Notification Hub Namespaces', 'web', 'web/Notification_Hub_Namespaces.svg'),
    'SearchService': ('Search Services', 'web', 'app_services/Search_Services.svg'),
    'SignalR': ('SignalR', 'web', 'web/SignalR.svg'),

    # ========== Security ==========
    'ApplicationSecurityGroup': ('Application Security Groups', 'security', 'security/Application_Security_Groups.svg'),
    'AzureADRiskySignin': ('Azure AD Risky Signins', 'security', 'security/Azure_AD_Risky_Signins.svg'),
    'AzureADRiskyUser': ('Azure AD Risky Users', 'security', 'security/Azure_AD_Risky_Users.svg'),
    'AzureDefender': ('Azure Defender', 'security', 'security/Azure_Defender.svg'),
    'AzureSentinel': ('Azure Sentinel', 'security', 'security/Azure_Sentinel.svg'),
    'ConditionalAccess': ('Conditional Access', 'security', 'security/Conditional_Access.svg'),
    'Detonation': ('Detonation', 'security', 'security/Detonation.svg'),
    'ExtendedSecurityUpdate': ('ExtendedSecurityUpdates', 'security', 'security/ExtendedSecurityUpdates.svg'),
    'IdentitySecureScore': ('Identity Secure Score', 'security', 'security/Identity_Secure_Score.svg'),
    'Key': ('Keys', 'security', 'security/Keys.svg'),
    'KeyVault': ('Key Vaults', 'security', 'security/Key_Vaults.svg'),
    'MSDefenderEASM': ('MS Defender EASM', 'security', 'security/MS_Defender_EASM.svg'),
    'MultifactorAuthentication': ('Multifactor Authentication', 'security', 'security/Multifactor_Authentication.svg'),
    'SecurityCenter': ('Security Center', 'security', 'security/Security_Center.svg'),

    # ========== Identity ==========
    'AADLicense': ('AAD Licenses', 'identity', 'identity/AAD_Licenses.svg'),
    'ActiveDirectoryConnectHealth': ('Active Directory Connect Health', 'identity', 'identity/Active_Directory_Connect_Health.svg'),
    'ActiveDirectoryConnectHealth2': ('Active Directory Connect Health2', 'identity', 'identity/Active_Directory_Connect_Health2.svg'),
    'AdministrativeUnit': ('Administrative Units', 'identity', 'identity/Administrative_Units.svg'),
    'AppRegistration': ('App Registrations', 'identity', 'identity/App_Registrations.svg'),
    'AzureADB2C': ('Azure AD B2C', 'identity', 'identity/Azure_AD_B2C.svg'),
    'AzureADB2C2': ('Azure AD B2C2', 'identity', 'identity/Azure_AD_B2C2.svg'),
    'AzureADDomainService': ('Azure AD Domain Services', 'identity', 'identity/Azure_AD_Domain_Services.svg'),
    'AzureADIdentityProtection': ('Azure AD Identity Protection', 'identity', 'identity/Azure_AD_Identity_Protection.svg'),
    'AzureADPrivilegeIdentityManagement': ('Azure AD Privilege Identity Management', 'identity', 'identity/Azure_AD_Privilege_Identity_Management.svg'),
    'AzureActiveDirectory': ('Azure Active Directory', 'identity', 'identity/Azure_Active_Directory.svg'),
    'AzureInformationProtection': ('Azure Information Protection', 'identity', 'identity/Azure_Information_Protection.svg'),
    'CustomAzureADRole': ('Custom Azure AD Roles', 'identity', 'identity/Custom_Azure_AD_Roles.svg'),
    'EnterpriseApplication': ('Enterprise Applications', 'identity', 'identity/Enterprise_Applications.svg'),
    'EntraConnect': ('Entra Connect', 'identity', 'identity/Entra_Connect.svg'),
    'EntraDomainService': ('Entra Domain Services', 'identity', 'identity/Entra_Domain_Services.svg'),
    'EntraGlobalSecureAccess': ('Entra Global Secure Access', 'identity', 'identity/Entra_Global_Secure_Access.svg'),
    'EntraIDProtection': ('Entra ID Protection', 'identity', 'identity/Entra_ID_Protection.svg'),
    'EntraInternetAccess': ('Entra Internet Access', 'identity', 'identity/Entra_Internet_Access.svg'),
    'EntraManagedIdentity': ('Entra Managed Identities', 'identity', 'identity/Entra_Managed_Identities.svg'),
    'EntraPrivateAccess': ('Entra Private Access', 'identity', 'identity/Entra_Private_Access.svg'),
    'EntraPrivilegedIdentityManagement': ('Entra Privileged Identity Management', 'identity', 'identity/Entra_Privileged_Identity_Management.svg'),
    'EntraVerifiedID': ('Entra Verified ID', 'identity', 'identity/Entra_Verified_ID.svg'),
    'ExternalIdentity': ('External Identities', 'identity', 'identity/External_Identities.svg'),
    'Group': ('Groups', 'identity', 'identity/Groups.svg'),
    'IdentityGovernance': ('Identity Governance', 'identity', 'identity/Identity_Governance.svg'),
    'ManagedIdentity': ('Managed Identities', 'identity', 'identity/Managed_Identities.svg'),
    'MultiFactorAuthentication': ('Multi Factor Authentication', 'identity', 'identity/Multi_Factor_Authentication.svg'),
    'PIM': ('PIM', 'identity', 'identity/PIM.svg'),
    'Security': ('Security', 'identity', 'identity/Security.svg'),
    'TenantProperty': ('Tenant Properties', 'identity', 'identity/Tenant_Properties.svg'),
    'User': ('Users', 'identity', 'identity/Users.svg'),
    'UserSetting': ('User Settings', 'identity', 'identity/User_Settings.svg'),
    'VerifiableCredential': ('Verifiable Credentials', 'identity', 'identity/Verifiable_Credentials.svg'),
    'VerificationAsAService': ('Verification As A Service', 'identity', 'identity/Verification_As_A_Service.svg'),

    # ========== Integration ==========
    'AppConfiguration': ('App Configuration', 'integration', 'integration/App_Configuration.svg'),
    'AzureAPIforFHIR': ('Azure API for FHIR', 'integration', 'integration/Azure_API_for_FHIR.svg'),
    'AzureDataCatalog': ('Azure Data Catalog', 'integration', 'integration/Azure_Data_Catalog.svg'),
    'EventGridDomain': ('Event Grid Domains', 'integration', 'integration/Event_Grid_Domains.svg'),
    'EventGridSubscription': ('Event Grid Subscriptions', 'integration', 'integration/Event_Grid_Subscriptions.svg'),
    'EventGridTopic': ('Event Grid Topics', 'integration', 'integration/Event_Grid_Topics.svg'),
    'IntegrationAPIManagementService': ('API Management Services', 'integration', 'integration/API_Management_Services.svg'),
    'IntegrationAccount': ('Integration Accounts', 'integration', 'integration/Integration_Accounts.svg'),
    'IntegrationEnvironment': ('Integration Environments', 'integration', 'integration/Integration_Environments.svg'),
    'IntegrationSQLDataWarehouse': ('SQL Data Warehouses', 'integration', 'integration/SQL_Data_Warehouses.svg'),
    'IntegrationServiceBus': ('Service Bus', 'integration', 'integration/Service_Bus.svg'),
    'IntegrationServiceEnvironment': ('Integration Service Environments', 'integration', 'integration/Integration_Service_Environments.svg'),
    'LogicApp': ('Logic Apps', 'integration', 'integration/Logic_Apps.svg'),
    'LogicAppsCustomConnector': ('Logic Apps Custom Connector', 'integration', 'integration/Logic_Apps_Custom_Connector.svg'),
    'PartnerNamespace': ('Partner Namespace', 'integration', 'integration/Partner_Namespace.svg'),
    'PartnerRegistration': ('Partner Registration', 'integration', 'integration/Partner_Registration.svg'),
    'PartnerTopic': ('Partner Topic', 'integration', 'integration/Partner_Topic.svg'),
    'Relay': ('Relays', 'integration', 'integration/Relays.svg'),
    'SendGridAccount': ('SendGrid Accounts', 'integration', 'integration/SendGrid_Accounts.svg'),
    'ServiceBus': ('Service Bus', 'integration', 'general/Service_Bus.svg'),
    'SoftwareasaService': ('Software as a Service', 'integration', 'integration/Software_as_a_Service.svg'),
    'SystemTopic': ('System Topic', 'integration', 'integration/System_Topic.svg'),

    # ========== Ai ==========
    'AIStudio': ('AI Studio', 'ai', 'ai_machine_learning/AI_Studio.svg'),
    'AnomalyDetector': ('Anomaly Detector', 'ai', 'ai_machine_learning/Anomaly_Detector.svg'),
    'AzureAppliedAI': ('Azure Applied AI', 'ai', 'ai_machine_learning/Azure_Applied_AI.svg'),
    'AzureExperimentationStudio': ('Azure Experimentation Studio', 'ai', 'ai_machine_learning/Azure_Experimentation_Studio.svg'),
    'AzureObjectUnderstanding': ('Azure Object Understanding', 'ai', 'ai_machine_learning/Azure_Object_Understanding.svg'),
    'AzureOpenAI': ('Azure OpenAI', 'ai', 'ai_machine_learning/Azure_OpenAI.svg'),
    'BatchAI': ('Batch AI', 'ai', 'ai_machine_learning/Batch_AI.svg'),
    'Bonsai': ('Bonsai', 'ai', 'ai_machine_learning/Bonsai.svg'),
    'BotService': ('Bot Services', 'ai', 'ai_machine_learning/Bot_Services.svg'),
    'CognitiveServices': ('Cognitive Services', 'ai', 'ai_machine_learning/Cognitive_Services.svg'),
    'CognitiveServicesDecisions': ('Cognitive Services Decisions', 'ai', 'ai_machine_learning/Cognitive_Services_Decisions.svg'),
    'ComputerVision': ('Computer Vision', 'ai', 'ai_machine_learning/Computer_Vision.svg'),
    'ContentModerator': ('Content Moderators', 'ai', 'ai_machine_learning/Content_Moderators.svg'),
    'ContentSafety': ('Content Safety', 'ai', 'ai_machine_learning/Content_Safety.svg'),
    'CustomVision': ('Custom Vision', 'ai', 'ai_machine_learning/Custom_Vision.svg'),
    'FaceAPI': ('Face APIs', 'ai', 'ai_machine_learning/Face_APIs.svg'),
    'FormRecognizer': ('Form Recognizers', 'ai', 'ai_machine_learning/Form_Recognizers.svg'),
    'Genomic': ('Genomics', 'ai', 'ai_machine_learning/Genomics.svg'),
    'ImmersiveReader': ('Immersive Readers', 'ai', 'ai_machine_learning/Immersive_Readers.svg'),
    'LanguageService': ('Language Services', 'ai', 'ai_machine_learning/Language_Services.svg'),
    'LanguageUnderstanding': ('Language Understanding', 'ai', 'ai_machine_learning/Language_Understanding.svg'),
    'MachineLearning': ('Machine Learning', 'ai', 'ai_machine_learning/Machine_Learning.svg'),
    'MachineLearningStudioClassicWebService': ('Machine Learning Studio Classic Web Services', 'ai', 'ai_machine_learning/Machine_Learning_Studio_Classic_Web_Services.svg'),
    'MachineLearningStudioWebServicePlan': ('Machine Learning Studio Web Service Plans', 'ai', 'ai_machine_learning/Machine_Learning_Studio_Web_Service_Plans.svg'),
    'MachineLearningStudioWorkspace': ('Machine Learning Studio Workspaces', 'ai', 'ai_machine_learning/Machine_Learning_Studio_Workspaces.svg'),
    'Personalizer': ('Personalizers', 'ai', 'ai_machine_learning/Personalizers.svg'),
    'QnAMaker': ('QnA Makers', 'ai', 'ai_machine_learning/QnA_Makers.svg'),
    'ServerlessSearch': ('Serverless Search', 'ai', 'ai_machine_learning/Serverless_Search.svg'),
    'SpeechService': ('Speech Services', 'ai', 'ai_machine_learning/Speech_Services.svg'),
    'TranslatorText': ('Translator Text', 'ai', 'ai_machine_learning/Translator_Text.svg'),

    # ========== Analytics ==========
    'AnalysisServices': ('Analysis Services', 'analytics', 'analytics/Analysis_Services.svg'),
    'AnalyticsAzureSynapseAnalytics': ('Azure Synapse Analytics', 'analytics', 'analytics/Azure_Synapse_Analytics.svg'),
    'AzureDatabrick': ('Azure Databricks', 'analytics', 'analytics/Azure_Databricks.svg'),
    'AzureWorkbook': ('Azure Workbooks', 'analytics', 'analytics/Azure_Workbooks.svg'),
    'DataLakeAnalytics': ('Data Lake Analytics', 'analytics', 'analytics/Data_Lake_Analytics.svg'),
    'DataLakeStoreGen1': ('Data Lake Store Gen1', 'analytics', 'analytics/Data_Lake_Store_Gen1.svg'),
    'EndpointAnalytics': ('Endpoint Analytics', 'analytics', 'analytics/Endpoint_Analytics.svg'),
    'EventHub': ('Event Hubs', 'analytics', 'analytics/Event_Hubs.svg'),
    'EventHubCluster': ('Event Hub Clusters', 'analytics', 'analytics/Event_Hub_Clusters.svg'),
    'HDInsightCluster': ('HD Insight Clusters', 'analytics', 'analytics/HD_Insight_Clusters.svg'),
    'LogAnalyticsWorkspaces': ('Log Analytics Workspaces', 'analytics', 'analytics/Log_Analytics_Workspaces.svg'),
    'PowerBIEmbedded': ('Power BI Embedded', 'analytics', 'analytics/Power_BI_Embedded.svg'),
    'PowerPlatform': ('Power Platform', 'analytics', 'analytics/Power_Platform.svg'),
    'StreamAnalyticsJobs': ('Stream Analytics Jobs', 'analytics', 'analytics/Stream_Analytics_Jobs.svg'),

    # ========== Devops ==========
    'APIConnection': ('API Connections', 'devops', 'devops/API_Connections.svg'),
    'ApplicationInsight': ('Application Insights', 'devops', 'devops/Application_Insights.svg'),
    'AzureDevOps': ('Azure DevOps', 'devops', 'devops/Azure_DevOps.svg'),
    'Backlog': ('Backlog', 'devops', 'general/Backlog.svg'),
    'Branch': ('Branch', 'devops', 'general/Branch.svg'),
    'Bug': ('Bug', 'devops', 'general/Bug.svg'),
    'Build': ('Builds', 'devops', 'general/Builds.svg'),
    'ChangeAnalysis': ('Change Analysis', 'devops', 'devops/Change_Analysis.svg'),
    'CloudTest': ('CloudTest', 'devops', 'devops/CloudTest.svg'),
    'Code': ('Code', 'devops', 'general/Code.svg'),
    'CodeOptimization': ('Code Optimization', 'devops', 'devops/Code_Optimization.svg'),
    'Commit': ('Commit', 'devops', 'general/Commit.svg'),
    'DevOpsStarter': ('DevOps Starter', 'devops', 'devops/DevOps_Starter.svg'),
    'DevTestLab': ('DevTest Labs', 'devops', 'devops/DevTest_Labs.svg'),
    'LabAccount': ('Lab Accounts', 'devops', 'devops/Lab_Accounts.svg'),
    'LabService': ('Lab Services', 'devops', 'devops/Lab_Services.svg'),

    # ========== Management ==========
    'ActivityLog': ('Activity Log', 'management', 'management_governance/Activity_Log.svg'),
    'Advisor': ('Advisor', 'management', 'management_governance/Advisor.svg'),
    'Alert': ('Alerts', 'management', 'management_governance/Alerts.svg'),
    'ArcMachine': ('Arc Machines', 'management', 'management_governance/Arc_Machines.svg'),
    'AutomationAccount': ('Automation Accounts', 'management', 'management_governance/Automation_Accounts.svg'),
    'AzureArc': ('Azure Arc', 'management', 'management_governance/Azure_Arc.svg'),
    'AzureLighthouse': ('Azure Lighthouse', 'management', 'management_governance/Azure_Lighthouse.svg'),
    'Blueprint': ('Blueprints', 'management', 'management_governance/Blueprints.svg'),
    'Compliance': ('Compliance', 'management', 'management_governance/Compliance.svg'),
    'CostAlert': ('Cost Alerts', 'management', 'general/Cost_Alerts.svg'),
    'CostAnalysis': ('Cost Analysis', 'management', 'general/Cost_Analysis.svg'),
    'CostBudget': ('Cost Budgets', 'management', 'general/Cost_Budgets.svg'),
    'CostManagement': ('Cost Management', 'management', 'general/Cost_Management.svg'),
    'CostManagementandBilling': ('Cost Management and Billing', 'management', 'general/Cost_Management_and_Billing.svg'),
    'CustomerLockboxforMSAzure': ('Customer Lockbox for MS Azure', 'management', 'management_governance/Customer_Lockbox_for_MS_Azure.svg'),
    'DiagnosticsSetting': ('Diagnostics Settings', 'management', 'management_governance/Diagnostics_Settings.svg'),
    'Education': ('Education', 'management', 'management_governance/Education.svg'),
    'MachinesAzureArc': ('MachinesAzureArc', 'management', 'management_governance/MachinesAzureArc.svg'),
    'ManagedApplicationsCenter': ('Managed Applications Center', 'management', 'management_governance/Managed_Applications_Center.svg'),
    'ManagedDesktop': ('Managed Desktop', 'management', 'management_governance/Managed_Desktop.svg'),
    'ManagementGroup': ('Management Groups', 'management', 'general/Management_Groups.svg'),
    'ManagementgovernanceApplicationInsight': ('Application Insights', 'management', 'management_governance/Application_Insights.svg'),
    'ManagementgovernanceCostManagementandBilling': ('Cost Management and Billing', 'management', 'management_governance/Cost_Management_and_Billing.svg'),
    'ManagementgovernanceLogAnalyticsWorkspaces': ('Log Analytics Workspaces', 'management', 'management_governance/Log_Analytics_Workspaces.svg'),
    'ManagementgovernanceRecoveryServicesVaults': ('Recovery Services Vaults', 'management', 'management_governance/Recovery_Services_Vaults.svg'),
    'Metric': ('Metrics', 'management', 'management_governance/Metrics.svg'),
    'Monitor': ('Monitor', 'management', 'management_governance/Monitor.svg'),
    'MyCustomer': ('My Customers', 'management', 'management_governance/My_Customers.svg'),
    'OperationLogClassic': ('Operation Log Classic', 'management', 'management_governance/Operation_Log_Classic.svg'),
    'Policy': ('Policy', 'management', 'management_governance/Policy.svg'),
    'ResourceGraphExplorer': ('Resource Graph Explorer', 'management', 'management_governance/Resource_Graph_Explorer.svg'),
    'ResourceGroup': ('Resource Groups', 'management', 'general/Resource_Groups.svg'),
    'ResourceGroupList': ('Resource Group List', 'management', 'general/Resource_Group_List.svg'),
    'ResourcesProvider': ('Resources Provider', 'management', 'management_governance/Resources_Provider.svg'),
    'SchedulerJobCollection': ('Scheduler Job Collections', 'management', 'management_governance/Scheduler_Job_Collections.svg'),
    'ServiceCatalogMAD': ('Service Catalog MAD', 'management', 'management_governance/Service_Catalog_MAD.svg'),
    'ServiceProvider': ('Service Providers', 'management', 'management_governance/Service_Providers.svg'),
    'Solution': ('Solutions', 'management', 'management_governance/Solutions.svg'),
    'Subscription': ('Subscriptions', 'management', 'general/Subscriptions.svg'),
    'UniversalPrint': ('Universal Print', 'management', 'management_governance/Universal_Print.svg'),
    'UserPrivacy': ('User Privacy', 'management', 'management_governance/User_Privacy.svg'),

    # ========== Iot ==========
    'AzureIoTOperation': ('Azure IoT Operations', 'iot', 'iot/Azure_IoT_Operations.svg'),
    'AzureMapsAccount': ('Azure Maps Accounts', 'iot', 'iot/Azure_Maps_Accounts.svg'),
    'AzureStackHCISizer': ('Azure Stack HCI Sizer', 'iot', 'iot/Azure_Stack_HCI_Sizer.svg'),
    'DeviceProvisioningService': ('Device Provisioning Services', 'iot', 'iot/Device_Provisioning_Services.svg'),
    'DigitalTwin': ('Digital Twins', 'iot', 'internet_of_things/Digital_Twins.svg'),
    'IndustrialIoT': ('Industrial IoT', 'iot', 'iot/Industrial_IoT.svg'),
    'InternetofthingsLogicApp': ('Logic Apps', 'iot', 'internet_of_things/Logic_Apps.svg'),
    'IoTCentralApplication': ('IoT Central Applications', 'iot', 'iot/IoT_Central_Applications.svg'),
    'IoTEdge': ('IoT Edge', 'iot', 'iot/IoT_Edge.svg'),
    'IoTHub': ('IoT Hub', 'iot', 'iot/IoT_Hub.svg'),
    'IotDigitalTwin': ('Digital Twins', 'iot', 'iot/Digital_Twins.svg'),
    'IotEventHub': ('Event Hubs', 'iot', 'iot/Event_Hubs.svg'),
    'IotFunctionApp': ('Function Apps', 'iot', 'iot/Function_Apps.svg'),
    'IotLogicApp': ('Logic Apps', 'iot', 'iot/Logic_Apps.svg'),
    'IotNotificationHub': ('Notification Hubs', 'iot', 'iot/Notification_Hubs.svg'),
    'IotStreamAnalyticsJobs': ('Stream Analytics Jobs', 'iot', 'iot/Stream_Analytics_Jobs.svg'),
    'StackHCIPremium': ('Stack HCI Premium', 'iot', 'iot/Stack_HCI_Premium.svg'),
    'TimeSeriesDataSet': ('Time Series Data Sets', 'iot', 'iot/Time_Series_Data_Sets.svg'),
    'TimeSeriesInsightsAccessPolicies': ('Time Series Insights Access Policies', 'iot', 'internet_of_things/Time_Series_Insights_Access_Policies.svg'),
    'TimeSeriesInsightsEnvironment': ('Time Series Insights Environments', 'iot', 'iot/Time_Series_Insights_Environments.svg'),
    'TimeSeriesInsightsEventSource': ('Time Series Insights Event Sources', 'iot', 'iot/Time_Series_Insights_Event_Sources.svg'),
    'Windows10CoreServices': ('Windows10 Core Services', 'iot', 'iot/Windows10_Core_Services.svg'),

    # ========== Monitor ==========
    'SAPAzureMonitor': ('SAP Azure Monitor', 'monitor', 'monitor/SAP_Azure_Monitor.svg'),

    # ========== Migrate ==========
    'AzureMigrate': ('Azure Migrate', 'migrate', 'migrate/Azure_Migrate.svg'),
    'MigrateCostManagementandBilling': ('Cost Management and Billing', 'migrate', 'migrate/Cost_Management_and_Billing.svg'),
    'MigrateDataBox': ('Data Box', 'migrate', 'migrate/Data_Box.svg'),
    'MigrateDataBoxEdge': ('Data Box Edge', 'migrate', 'migrate/Data_Box_Edge.svg'),
    'MigrateRecoveryServicesVaults': ('Recovery Services Vaults', 'migrate', 'migrate/Recovery_Services_Vaults.svg'),

    # ========== Vmware ==========
    'AVS': ('AVS', 'vmware', 'azure_vmware_solution/AVS.svg'),

    # ========== Azure_stack ==========
    'AzureStack': ('Azure Stack', 'azure_stack', 'azure_stack/Azure_Stack.svg'),
    'Capacity': ('Capacity', 'azure_stack', 'azure_stack/Capacity.svg'),
    'InfrastructureBackup': ('Infrastructure Backup', 'azure_stack', 'azure_stack/Infrastructure_Backup.svg'),
    'MultiTenancy': ('Multi Tenancy', 'azure_stack', 'azure_stack/Multi_Tenancy.svg'),
    'Offer': ('Offers', 'azure_stack', 'azure_stack/Offers.svg'),
    'Plan': ('Plans', 'azure_stack', 'azure_stack/Plans.svg'),
    'Update': ('Updates', 'azure_stack', 'azure_stack/Updates.svg'),
    'UserSubscription': ('User Subscriptions', 'azure_stack', 'azure_stack/User_Subscriptions.svg'),

    # ========== Blockchain ==========
    'ABSMember': ('ABS Member', 'blockchain', 'blockchain/ABS_Member.svg'),
    'AzureBlockchainService': ('Azure Blockchain Service', 'blockchain', 'blockchain/Azure_Blockchain_Service.svg'),
    'AzureTokenService': ('Azure Token Service', 'blockchain', 'blockchain/Azure_Token_Service.svg'),
    'BlockchainApplication': ('Blockchain Applications', 'blockchain', 'blockchain/Blockchain_Applications.svg'),
    'Consortium': ('Consortium', 'blockchain', 'blockchain/Consortium.svg'),
    'OutboundConnection': ('Outbound Connection', 'blockchain', 'blockchain/Outbound_Connection.svg'),

    # ========== Mixed_reality ==========
    'RemoteRendering': ('Remote Rendering', 'mixed_reality', 'mixed_reality/Remote_Rendering.svg'),
    'SpatialAnchorAccount': ('Spatial Anchor Accounts', 'mixed_reality', 'mixed_reality/Spatial_Anchor_Accounts.svg'),

    # ========== Intune ==========
    'AzureADRolesandAdministrator': ('Azure AD Roles and Administrators', 'intune', 'intune/Azure_AD_Roles_and_Administrators.svg'),
    'ClientApp': ('Client Apps', 'intune', 'intune/Client_Apps.svg'),
    'Device': ('Devices', 'intune', 'intune/Devices.svg'),
    'DeviceCompliance': ('Device Compliance', 'intune', 'intune/Device_Compliance.svg'),
    'DeviceConfiguration': ('Device Configuration', 'intune', 'intune/Device_Configuration.svg'),
    'DeviceEnrollment': ('Device Enrollment', 'intune', 'intune/Device_Enrollment.svg'),
    'DeviceSecurityApple': ('Device Security Apple', 'intune', 'intune/Device_Security_Apple.svg'),
    'DeviceSecurityGoogle': ('Device Security Google', 'intune', 'intune/Device_Security_Google.svg'),
    'DeviceSecurityWindows': ('Device Security Windows', 'intune', 'intune/Device_Security_Windows.svg'),
    'ExchangeAccess': ('Exchange Access', 'intune', 'intune/Exchange_Access.svg'),
    'Intune': ('Intune', 'intune', 'intune/Intune.svg'),
    'IntuneForEducation': ('Intune For Education', 'intune', 'intune/Intune_For_Education.svg'),
    'Mindaro': ('Mindaro', 'intune', 'intune/Mindaro.svg'),
    'SecurityBaseline': ('Security Baselines', 'intune', 'intune/Security_Baselines.svg'),
    'SoftwareUpdate': ('Software Updates', 'intune', 'intune/Software_Updates.svg'),
    'TenantStatus': ('Tenant Status', 'intune', 'intune/Tenant_Status.svg'),
    'eBook': ('eBooks', 'intune', 'intune/eBooks.svg'),

    # ========== Hybrid ==========
    'AzureOperator5GCore': ('Azure Operator 5G Core', 'hybrid', 'hybrid_multicloud/Azure_Operator_5G_Core.svg'),
    'AzureOperatorInsight': ('Azure Operator Insights', 'hybrid', 'hybrid_multicloud/Azure_Operator_Insights.svg'),
    'AzureOperatorNexus': ('Azure Operator Nexus', 'hybrid', 'hybrid_multicloud/Azure_Operator_Nexus.svg'),
    'AzureOperatorServiceManager': ('Azure Operator Service Manager', 'hybrid', 'hybrid_multicloud/Azure_Operator_Service_Manager.svg'),
    'AzureProgrammableConnectivity': ('Azure Programmable Connectivity', 'hybrid', 'hybrid_multicloud/Azure_Programmable_Connectivity.svg'),

    # ========== Power_platform ==========
    'AIBuilder': ('AIBuilder', 'power_platform', 'power_platform/AIBuilder.svg'),
    'CopilotStudio': ('CopilotStudio', 'power_platform', 'power_platform/CopilotStudio.svg'),
    'Dataverse': ('Dataverse', 'power_platform', 'power_platform/Dataverse.svg'),
    'PowerApp': ('PowerApps', 'power_platform', 'power_platform/PowerApps.svg'),
    'PowerAutomate': ('PowerAutomate', 'power_platform', 'power_platform/PowerAutomate.svg'),
    'PowerBI': ('PowerBI', 'power_platform', 'power_platform/PowerBI.svg'),
    'PowerFx': ('PowerFx', 'power_platform', 'power_platform/PowerFx.svg'),
    'PowerPage': ('PowerPages', 'power_platform', 'power_platform/PowerPages.svg'),
    'PowerplatformPowerPlatform': ('PowerPlatform', 'power_platform', 'power_platform/PowerPlatform.svg'),

    # ========== Preview ==========
    'AzureCloudShell': ('Azure Cloud Shell', 'preview', 'preview/Azure_Cloud_Shell.svg'),
    'AzureSphere': ('Azure Sphere', 'preview', 'preview/Azure_Sphere.svg'),
    'PreviewAzureWorkbook': ('Azure Workbooks', 'preview', 'preview/Azure_Workbooks.svg'),
    'PreviewIoTEdge': ('IoT Edge', 'preview', 'preview/IoT_Edge.svg'),
    'PreviewPrivateLinkHub': ('Private Link Hub', 'preview', 'preview/Private_Link_Hub.svg'),
    'PreviewTimeSeriesDataSet': ('Time Series Data Sets', 'preview', 'preview/Time_Series_Data_Sets.svg'),
    'RTOS': ('RTOS', 'preview', 'preview/RTOS.svg'),
    'StaticApp': ('Static Apps', 'preview', 'preview/Static_Apps.svg'),
    'WebEnvironment': ('Web Environment', 'preview', 'preview/Web_Environment.svg'),

    # ========== Other ==========
    'ACSSolutionsBuilder': ('ACS Solutions Builder', 'other', 'other/ACS_Solutions_Builder.svg'),
    'AKSAutomatic': ('AKS Automatic', 'other', 'other/AKS_Automatic.svg'),
    'AKSIstio': ('AKS Istio', 'other', 'other/AKS_Istio.svg'),
    'APIProxy': ('API Proxy', 'other', 'other/API_Proxy.svg'),
    'AppComplianceAutomation': ('App Compliance Automation', 'other', 'other/App_Compliance_Automation.svg'),
    'AppSpaceComponent': ('App Space Component', 'other', 'other/App_Space_Component.svg'),
    'Aquila': ('Aquila', 'other', 'other/Aquila.svg'),
    'ArcDataservice': ('Arc Data services', 'other', 'other/Arc_Data_services.svg'),
    'ArcKubernetes': ('Arc Kubernetes', 'other', 'other/Arc_Kubernetes.svg'),
    'ArcPostgreSQL': ('Arc PostgreSQL', 'other', 'other/Arc_PostgreSQL.svg'),
    'ArcSQLManagedInstance': ('Arc SQL Managed Instance', 'other', 'other/Arc_SQL_Managed_Instance.svg'),
    'ArcSQLServer': ('Arc SQL Server', 'other', 'other/Arc_SQL_Server.svg'),
    'AzureA': ('Azure A', 'other', 'other/Azure_A.svg'),
    'AzureAttestation': ('AzureAttestation', 'other', 'other/AzureAttestation.svg'),
    'AzureBackupCenter': ('Azure Backup Center', 'other', 'other/Azure_Backup_Center.svg'),
    'AzureCenterforSAP': ('Azure Center for SAP', 'other', 'other/Azure_Center_for_SAP.svg'),
    'AzureChaosStudio': ('Azure Chaos Studio', 'other', 'other/Azure_Chaos_Studio.svg'),
    'AzureCommunicationService': ('Azure Communication Services', 'other', 'other/Azure_Communication_Services.svg'),
    'AzureDeploymentEnvironment': ('Azure Deployment Environments', 'other', 'other/Azure_Deployment_Environments.svg'),
    'AzureDevTunnel': ('Azure Dev Tunnels', 'other', 'other/Azure_Dev_Tunnels.svg'),
    'AzureEdgeHardwareCenter': ('Azure Edge Hardware Center', 'other', 'other/Azure_Edge_Hardware_Center.svg'),
    'AzureHPCWorkbench': ('Azure HPC Workbench', 'other', 'other/Azure_HPC_Workbench.svg'),
    'AzureLoadTesting': ('Azure Load Testing', 'other', 'other/Azure_Load_Testing.svg'),
    'AzureMonitorDashboard': ('Azure Monitor Dashboard', 'other', 'other/Azure_Monitor_Dashboard.svg'),
    'AzureMonitorPipeline': ('Azure Monitor Pipeline', 'other', 'other/Azure_Monitor_Pipeline.svg'),
    'AzureNetworkFunctionManager': ('Azure Network Function Manager', 'other', 'other/Azure_Network_Function_Manager.svg'),
    'AzureNetworkFunctionManagerFunction': ('Azure Network Function Manager Functions', 'other', 'other/Azure_Network_Function_Manager_Functions.svg'),
    'AzureNetworkManager': ('Azure Network Manager', 'other', 'other/Azure_Network_Manager.svg'),
    'AzureOrbital': ('Azure Orbital', 'other', 'other/Azure_Orbital.svg'),
    'AzureQuota': ('Azure Quotas', 'other', 'other/Azure_Quotas.svg'),
    'AzureStorageMover': ('Azure Storage Mover', 'other', 'other/Azure_Storage_Mover.svg'),
    'AzureSupportCenterBlue': ('Azure Support Center Blue', 'other', 'other/Azure_Support_Center_Blue.svg'),
    'AzureSustainability': ('Azure Sustainability', 'other', 'other/Azure_Sustainability.svg'),
    'AzureVideoIndexer': ('Azure Video Indexer', 'other', 'other/Azure_Video_Indexer.svg'),
    'Azurite': ('Azurite', 'other', 'other/Azurite.svg'),
    'BackupVault': ('Backup Vault', 'other', 'other/Backup_Vault.svg'),
    'BareMetalInfrastructure': ('Bare Metal Infrastructure', 'other', 'other/Bare_Metal_Infrastructure.svg'),
    'BusinessProcessTracking': ('Business Process Tracking', 'other', 'other/Business_Process_Tracking.svg'),
    'CentralServiceInstanceforSAP': ('Central Service Instance for SAP', 'other', 'other/Central_Service_Instance_for_SAP.svg'),
    'Cere': ('Ceres', 'other', 'other/Ceres.svg'),
    'CloudServices(extendedsupport)': ('Cloud Services (extended support)', 'other', 'other/Cloud_Services_(extended_support).svg'),
    'ComplianceCenter': ('Compliance Center', 'other', 'other/Compliance_Center.svg'),
    'ComputeFleet': ('Compute Fleet', 'other', 'other/Compute_Fleet.svg'),
    'ConfidentialLedger': ('Confidential Ledger', 'other', 'other/Confidential_Ledger.svg'),
    'ConnectedCache': ('Connected Cache', 'other', 'other/Connected_Cache.svg'),
    'ConnectedVehiclePlatform': ('Connected Vehicle Platform', 'other', 'other/Connected_Vehicle_Platform.svg'),
    'ContainerAppEnvironment': ('Container App Environments', 'other', 'other/Container_App_Environments.svg'),
    'CostExport': ('Cost Export', 'other', 'other/Cost_Export.svg'),
    'CustomIPPrefix': ('Custom IP Prefix', 'other', 'other/Custom_IP_Prefix.svg'),
    'DashboardHub': ('Dashboard Hub', 'other', 'other/Dashboard_Hub.svg'),
    'DataCollectionRule': ('Data Collection Rules', 'other', 'other/Data_Collection_Rules.svg'),
    'DatabaseInstanceForSAP': ('Database Instance For SAP', 'other', 'other/Database_Instance_For_SAP.svg'),
    'DedicatedHSM': ('Dedicated HSM', 'other', 'other/Dedicated_HSM.svg'),
    'DefenderCMLocalManager': ('Defender CM Local Manager', 'other', 'other/Defender_CM_Local_Manager.svg'),
    'DefenderDCSController': ('Defender DCS Controller', 'other', 'other/Defender_DCS_Controller.svg'),
    'DefenderDistributerControlSystem': ('Defender Distributer Control System', 'other', 'other/Defender_Distributer_Control_System.svg'),
    'DefenderEngineeringStation': ('Defender Engineering Station', 'other', 'other/Defender_Engineering_Station.svg'),
    'DefenderExternalManagement': ('Defender External Management', 'other', 'other/Defender_External_Management.svg'),
    'DefenderFreezerMonitor': ('Defender Freezer Monitor', 'other', 'other/Defender_Freezer_Monitor.svg'),
    'DefenderHMI': ('Defender HMI', 'other', 'other/Defender_HMI.svg'),
    'DefenderHistorian': ('Defender Historian', 'other', 'other/Defender_Historian.svg'),
    'DefenderIndustrialPackagingSystem': ('Defender Industrial Packaging System', 'other', 'other/Defender_Industrial_Packaging_System.svg'),
    'DefenderIndustrialPrinter': ('Defender Industrial Printer', 'other', 'other/Defender_Industrial_Printer.svg'),
    'DefenderIndustrialRobot': ('Defender Industrial Robot', 'other', 'other/Defender_Industrial_Robot.svg'),
    'DefenderIndustrialScaleSystem': ('Defender Industrial Scale System', 'other', 'other/Defender_Industrial_Scale_System.svg'),
    'DefenderMarquee': ('Defender Marquee', 'other', 'other/Defender_Marquee.svg'),
    'DefenderMeter': ('Defender Meter', 'other', 'other/Defender_Meter.svg'),
    'DefenderPLC': ('Defender PLC', 'other', 'other/Defender_PLC.svg'),
    'DefenderPneumaticDevice': ('Defender Pneumatic Device', 'other', 'other/Defender_Pneumatic_Device.svg'),
    'DefenderProgramableBoard': ('Defender Programable Board', 'other', 'other/Defender_Programable_Board.svg'),
    'DefenderRTU': ('Defender RTU', 'other', 'other/Defender_RTU.svg'),
    'DefenderRelay': ('Defender Relay', 'other', 'other/Defender_Relay.svg'),
    'DefenderRobotController': ('Defender Robot Controller', 'other', 'other/Defender_Robot_Controller.svg'),
    'DefenderSensor': ('Defender Sensor', 'other', 'other/Defender_Sensor.svg'),
    'DefenderSlot': ('Defender Slot', 'other', 'other/Defender_Slot.svg'),
    'DefenderWebGuidingSystem': ('Defender Web Guiding System', 'other', 'other/Defender_Web_Guiding_System.svg'),
    'DeviceUpdateIoTHub': ('Device Update IoT Hub', 'other', 'other/Device_Update_IoT_Hub.svg'),
    'DiskPool': ('Disk Pool', 'other', 'other/Disk_Pool.svg'),
    'EdgeManagement': ('Edge Management', 'other', 'other/Edge_Management.svg'),
    'ElasticSAN': ('Elastic SAN', 'other', 'other/Elastic_SAN.svg'),
    'Elixir': ('Elixir', 'other', 'cxp/Elixir.svg'),
    'ElixirPurple': ('Elixir Purple', 'other', 'cxp/Elixir_Purple.svg'),
    'EntraConnectHealth': ('Entra Connect Health', 'other', 'other/Entra_Connect_Health.svg'),
    'EntraConnectSync': ('Entra Connect Sync', 'other', 'other/Entra_Connect_Sync.svg'),
    'EntraIdentity': ('Entra Identity', 'other', 'other/Entra_Identity.svg'),
    'ExchangeOnPremisesAccess': ('Exchange On Premises Access', 'other', 'other/Exchange_On_Premises_Access.svg'),
    'ExpressRouteDirect': ('ExpressRoute Direct', 'other', 'other/ExpressRoute_Direct.svg'),
    'ExpressRouteTrafficCollector': ('Express Route Traffic Collector', 'other', 'other/Express_Route_Traffic_Collector.svg'),
    'FHIRService': ('FHIR Service', 'other', 'other/FHIR_Service.svg'),
    'Fiji': ('Fiji', 'other', 'other/Fiji.svg'),
    'Grafana': ('Grafana', 'other', 'other/Grafana.svg'),
    'HDIAKSCluster': ('HDI AKS Cluster', 'other', 'other/HDI_AKS_Cluster.svg'),
    'IcMTroubleshooting': ('IcM Troubleshooting', 'other', 'other/IcM_Troubleshooting.svg'),
    'InternetAnalyzerProfile': ('Internet Analyzer Profiles', 'other', 'other/Internet_Analyzer_Profiles.svg'),
    'IntuneTrend': ('Intune Trends', 'other', 'other/Intune_Trends.svg'),
    'KubernetesFleetManager': ('Kubernetes Fleet Manager', 'other', 'other/Kubernetes_Fleet_Manager.svg'),
    'LoadTesting': ('Load Testing', 'other', 'other/Load_Testing.svg'),
    'LogAnalyticsQueryPack': ('Log Analytics Query Pack', 'other', 'other/Log_Analytics_Query_Pack.svg'),
    'MSDevBox': ('MS Dev Box', 'other', 'other/MS_Dev_Box.svg'),
    'ManagedDevOpsPools': ('Managed DevOps Pools', 'other', 'other/Managed_DevOps_Pools.svg'),
    'ManagedFileShare': ('Managed File Shares', 'other', 'other/Managed_File_Shares.svg'),
    'ManagedInstanceApacheCassandra': ('Managed Instance Apache Cassandra', 'other', 'other/Managed_Instance_Apache_Cassandra.svg'),
    'MarketplaceManagement': ('Marketplace Management', 'other', 'other/Marketplace_Management.svg'),
    'MedTechService': ('MedTech Service', 'other', 'other/MedTech_Service.svg'),
    'MenuKey': ('Keys', 'other', 'menu/Keys.svg'),
    'MissionLandingZone': ('Mission Landing Zone', 'other', 'other/Mission_Landing_Zone.svg'),
    'ModularDataCenter': ('Modular Data Center', 'other', 'other/Modular_Data_Center.svg'),
    'MonitorHealthModel': ('Monitor Health Models', 'other', 'other/Monitor_Health_Models.svg'),
    'NetworkSecurityPerimeter': ('Network Security Perimeters', 'other', 'other/Network_Security_Perimeters.svg'),
    'OSConfig': ('OSConfig', 'other', 'other/OSConfig.svg'),
    'OpenSupplyChainPlatform': ('Open Supply Chain Platform', 'other', 'other/Open_Supply_Chain_Platform.svg'),
    'OtherAzureCloudShell': ('Azure Cloud Shell', 'other', 'other/Azure_Cloud_Shell.svg'),
    'OtherAzureSphere': ('Azure Sphere', 'other', 'other/Azure_Sphere.svg'),
    'OtherDetonation': ('Detonation', 'other', 'other/Detonation.svg'),
    'OtherImageDefinition': ('Image Definition', 'other', 'other/Image_Definition.svg'),
    'OtherImageVersion': ('Image Version', 'other', 'other/Image_Version.svg'),
    'OtherInstancePool': ('Instance Pools', 'other', 'other/Instance_Pools.svg'),
    'OtherLocalNetworkGateway': ('Local Network Gateways', 'other', 'other/Local_Network_Gateways.svg'),
    'OtherPrivateEndpoint': ('Private Endpoints', 'other', 'other/Private_Endpoints.svg'),
    'OtherRTOS': ('RTOS', 'other', 'other/RTOS.svg'),
    'OtherUniversalPrint': ('Universal Print', 'other', 'other/Universal_Print.svg'),
    'Peering': ('Peerings', 'other', 'other/Peerings.svg'),
    'PeeringService': ('Peering Service', 'other', 'other/Peering_Service.svg'),
    'PrivateMobileNetwork': ('Private Mobile Network', 'other', 'other/Private_Mobile_Network.svg'),
    'ReservedCapacity': ('Reserved Capacity', 'other', 'other/Reserved_Capacity.svg'),
    'ReservedCapacityGroup': ('Reserved Capacity Groups', 'other', 'other/Reserved_Capacity_Groups.svg'),
    'ResourceGuard': ('Resource Guard', 'other', 'other/Resource_Guard.svg'),
    'ResourceMover': ('Resource Mover', 'other', 'other/Resource_Mover.svg'),
    'SSHKey': ('SSH Keys', 'other', 'other/SSH_Keys.svg'),
    'SavingsPlan': ('Savings Plan', 'other', 'other/Savings_Plan.svg'),
    'SonicDash': ('Sonic Dash', 'other', 'other/Sonic_Dash.svg'),
    'StorageAction': ('Storage Actions', 'other', 'other/Storage_Actions.svg'),
    'StorageTask': ('Storage Tasks', 'other', 'other/Storage_Tasks.svg'),
    'TargetsManagement': ('Targets Management', 'other', 'other/Targets_Management.svg'),
    'TemplateSpec': ('Template Specs', 'other', 'other/Template_Specs.svg'),
    'TestBase': ('Test Base', 'other', 'other/Test_Base.svg'),
    'UpdateCenter': ('Update Center', 'other', 'other/Update_Center.svg'),
    'VideoAnalyzer': ('Video Analyzers', 'other', 'other/Video_Analyzers.svg'),
    'VirtualEnclave': ('Virtual Enclaves', 'other', 'other/Virtual_Enclaves.svg'),
    'VirtualInstanceforSAP': ('Virtual Instance for SAP', 'other', 'other/Virtual_Instance_for_SAP.svg'),
    'WAC': ('WAC', 'other', 'other/WAC.svg'),
    'WACInstaller': ('WAC Installer', 'other', 'other/WAC_Installer.svg'),
    'WebAppDatabase': ('Web App Database', 'other', 'other/Web_App_Database.svg'),
    'WebJob': ('Web Jobs', 'other', 'other/Web_Jobs.svg'),
    'WindowsNotificationServices': ('Windows Notification Services', 'other', 'other/Windows_Notification_Services.svg'),
    'WindowsVirtualDesktop': ('Windows Virtual Desktop', 'other', 'other/Windows_Virtual_Desktop.svg'),
    'WorkerContainerApp': ('Worker Container App', 'other', 'other/Worker_Container_App.svg'),
    'WorkspaceGateway': ('Workspace Gateway', 'other', 'other/Workspace_Gateway.svg'),

    # ========== General ==========
    'AllResource': ('All Resources', 'general', 'general/All_Resources.svg'),
    'Applen': ('Applens', 'general', 'azure_ecosystem/Applens.svg'),
    'AzureHybridCenter': ('Azure Hybrid Center', 'general', 'azure_ecosystem/Azure_Hybrid_Center.svg'),
    'BizTalk': ('Biz Talk', 'general', 'general/Biz_Talk.svg'),
    'Browser': ('Browser', 'general', 'general/Browser.svg'),
    'Cache': ('Cache', 'general', 'general/Cache.svg'),
    'CollaborativeService': ('Collaborative Service', 'general', 'azure_ecosystem/Collaborative_Service.svg'),
    'Control': ('Controls', 'general', 'general/Controls.svg'),
    'ControlsHorizontal': ('Controls Horizontal', 'general', 'general/Controls_Horizontal.svg'),
    'Counter': ('Counter', 'general', 'general/Counter.svg'),
    'Cube': ('Cubes', 'general', 'general/Cubes.svg'),
    'Dashboard': ('Dashboard', 'general', 'general/Dashboard.svg'),
    'Dashboard2': ('Dashboard2', 'general', 'general/Dashboard2.svg'),
    'DevConsole': ('Dev Console', 'general', 'general/Dev_Console.svg'),
    'Download': ('Download', 'general', 'general/Download.svg'),
    'Error': ('Error', 'general', 'general/Error.svg'),
    'Extension': ('Extensions', 'general', 'general/Extensions.svg'),
    'FTP': ('FTP', 'general', 'general/FTP.svg'),
    'File': ('File', 'general', 'general/File.svg'),
    'FolderBlank': ('Folder Blank', 'general', 'general/Folder_Blank.svg'),
    'FolderWebsite': ('Folder Website', 'general', 'general/Folder_Website.svg'),
    'FreeService': ('Free Services', 'general', 'general/Free_Services.svg'),
    'Gear': ('Gear', 'general', 'general/Gear.svg'),
    'GeneralFile': ('Files', 'general', 'general/Files.svg'),
    'GeneralImage': ('Image', 'general', 'general/Image.svg'),
    'GeneralTag': ('Tags', 'general', 'general/Tags.svg'),
    'Globe': ('Globe', 'general', 'general/Globe.svg'),
    'GlobeError': ('Globe Error', 'general', 'general/Globe_Error.svg'),
    'GlobeSuccess': ('Globe Success', 'general', 'general/Globe_Success.svg'),
    'GlobeWarning': ('Globe Warning', 'general', 'general/Globe_Warning.svg'),
    'Guide': ('Guide', 'general', 'general/Guide.svg'),
    'Heart': ('Heart', 'general', 'general/Heart.svg'),
    'HelpandSupport': ('Help and Support', 'general', 'general/Help_and_Support.svg'),
    'Information': ('Information', 'general', 'general/Information.svg'),
    'InputOutput': ('Input Output', 'general', 'general/Input_Output.svg'),
    'JourneyHub': ('Journey Hub', 'general', 'general/Journey_Hub.svg'),
    'LaunchPortal': ('Launch Portal', 'general', 'general/Launch_Portal.svg'),
    'Learn': ('Learn', 'general', 'general/Learn.svg'),
    'LoadTest': ('Load Test', 'general', 'general/Load_Test.svg'),
    'Location': ('Location', 'general', 'general/Location.svg'),
    'LogStreaming': ('Log Streaming', 'general', 'general/Log_Streaming.svg'),
    'ManagementPortal': ('Management Portal', 'general', 'general/Management_Portal.svg'),
    'Marketplace': ('Marketplace', 'general', 'general/Marketplace.svg'),
    'Media': ('Media', 'general', 'general/Media.svg'),
    'MediaFile': ('Media File', 'general', 'general/Media_File.svg'),
    'Mobile': ('Mobile', 'general', 'general/Mobile.svg'),
    'MobileEngagement': ('Mobile Engagement', 'general', 'general/Mobile_Engagement.svg'),
    'Module': ('Module', 'general', 'general/Module.svg'),
    'Power': ('Power', 'general', 'general/Power.svg'),
    'PowerUp': ('Power Up', 'general', 'general/Power_Up.svg'),
    'Powershell': ('Powershell', 'general', 'general/Powershell.svg'),
    'Preview': ('Preview', 'general', 'general/Preview.svg'),
    'PreviewFeature': ('Preview Features', 'general', 'general/Preview_Features.svg'),
    'ProcessExplorer': ('Process Explorer', 'general', 'general/Process_Explorer.svg'),
    'ProductionReadyDatabase': ('Production Ready Database', 'general', 'general/Production_Ready_Database.svg'),
    'QuickstartCenter': ('Quickstart Center', 'general', 'general/Quickstart_Center.svg'),
    'Recent': ('Recent', 'general', 'general/Recent.svg'),
    'Reservation': ('Reservations', 'general', 'general/Reservations.svg'),
    'ResourceExplorer': ('Resource Explorer', 'general', 'general/Resource_Explorer.svg'),
    'ResourceLinked': ('Resource Linked', 'general', 'general/Resource_Linked.svg'),
    'SSD': ('SSD', 'general', 'general/SSD.svg'),
    'Scale': ('Scale', 'general', 'general/Scale.svg'),
    'Scheduler': ('Scheduler', 'general', 'general/Scheduler.svg'),
    'Search': ('Search', 'general', 'general/Search.svg'),
    'SearchGrid': ('Search Grid', 'general', 'general/Search_Grid.svg'),
    'ServerFarm': ('Server Farm', 'general', 'general/Server_Farm.svg'),
    'ServiceHealth': ('Service Health', 'general', 'general/Service_Health.svg'),
    'TFSVCRepository': ('TFS VC Repository', 'general', 'general/TFS_VC_Repository.svg'),
    'Table': ('Table', 'general', 'general/Table.svg'),
    'Tag': ('Tag', 'general', 'general/Tag.svg'),
    'Template': ('Templates', 'general', 'general/Templates.svg'),
    'Toolbox': ('Toolbox', 'general', 'general/Toolbox.svg'),
    'Troubleshoot': ('Troubleshoot', 'general', 'general/Troubleshoot.svg'),
    'Version': ('Versions', 'general', 'general/Versions.svg'),
    'WebSlot': ('Web Slots', 'general', 'general/Web_Slots.svg'),
    'WebTest': ('Web Test', 'general', 'general/Web_Test.svg'),
    'WebsitePower': ('Website Power', 'general', 'general/Website_Power.svg'),
    'WebsiteStaging': ('Website Staging', 'general', 'general/Website_Staging.svg'),
    'Workbook': ('Workbooks', 'general', 'general/Workbooks.svg'),
    'Workflow': ('Workflow', 'general', 'general/Workflow.svg'),

}

# Alias mapping for common/intuitive names to actual AZURE_SHAPES keys
# This helps when users type natural names that don't match exactly
RESOURCE_TYPE_ALIASES: Dict[str, str] = {
    # Storage aliases
    'BlobStorage': 'BlobBlock',
    'Blob': 'BlobBlock',
    'FileStorage': 'StorageAzureFiles',
    'Files': 'StorageAzureFiles',
    'AzureFiles': 'StorageAzureFiles',
    'Storage': 'StorageAccount',
    'Queue': 'StorageQueue',
    'StorageBlob': 'BlobBlock',
    
    # Monitoring aliases
    'ApplicationInsights': 'ApplicationInsight',
    'AppInsights': 'ApplicationInsight',
    'Insights': 'ApplicationInsight',
    'AzureMonitor': 'Monitor',
    'LogAnalytics': 'LogAnalyticsWorkspaces',
    'Logs': 'LogAnalyticsWorkspaces',
    'ActivityLogs': 'ActivityLog',
    
    # Compute aliases
    'VM': 'VirtualMachine',
    'VMs': 'VirtualMachine',
    'AKS': 'KubernetesServices',
    'Kubernetes': 'KubernetesServices',
    'K8s': 'KubernetesServices',
    'WebApp': 'AppService',
    'App': 'AppService',
    'Functions': 'FunctionApp',
    'Function': 'FunctionApp',
    'AzureFunctions': 'FunctionApp',
    'ContainerInstance': 'ContainerInstance',
    'ACI': 'ContainerInstance',
    'ACR': 'ContainerRegistry',
    'ContainerRegistries': 'ContainerRegistry',
    
    # Database aliases
    'SQL': 'AzureSQL',
    'SQLDatabase': 'AzureSQL',
    'SQLDB': 'AzureSQL',
    'Cosmos': 'AzureCosmosDB',
    'CosmosDB': 'AzureCosmosDB',
    'Redis': 'CacheRedis',
    'RedisCache': 'CacheRedis',
    'Cache': 'CacheRedis',
    'MySQL': 'AzureDatabaseMySQLServer',
    'PostgreSQL': 'AzureDatabasePostgreSQLServer',
    'Postgres': 'AzureDatabasePostgreSQLServer',
    
    # Network aliases  
    'FrontDoor': 'FrontDoor',
    'AFD': 'FrontDoor',
    'CDN': 'CDNProfile',
    'AzureCDN': 'CDNProfile',
    'DNS': 'AzureDns',
    'DNSZone': 'DNSZone',
    'WAF': 'WebApplicationFirewallPoliciesWAF',
    'Firewall': 'AzureFirewall',
    'VNet': 'VirtualNetwork',
    'VNET': 'VirtualNetwork',
    'VirtualNetwork': 'VirtualNetwork',
    'LoadBalancer': 'LoadBalancers',
    'LB': 'LoadBalancers',
    'AppGateway': 'ApplicationGateway',
    'AGW': 'ApplicationGateway',
    'TrafficManager': 'TrafficManager',
    'VPN': 'VPNGateway',
    'ExpressRoute': 'ExpressRouteCircuit',
    'Bastion': 'Bastion',
    'PrivateLink': 'PrivateLink',
    'PrivateEndpoint': 'PrivateEndpoints',
    'NSG': 'NetworkSecurityGroups',
    
    # Identity aliases
    'AAD': 'AzureActiveDirectory',
    'AzureAD': 'AzureActiveDirectory',
    'EntraID': 'AzureActiveDirectory',
    'ActiveDirectory': 'AzureActiveDirectory',
    'ManagedIdentity': 'ManagedIdentities',
    'Identity': 'ManagedIdentities',
    
    # Messaging aliases
    'ServiceBus': 'ServiceBus',
    'EventHub': 'EventHub',
    'EventHubs': 'EventHub',
    'EventGrid': 'EventGrid',
    'SignalR': 'SignalR',
    
    # AI/ML aliases
    'OpenAI': 'AzureOpenAI',
    'CognitiveServices': 'CognitiveServices',
    'AIServices': 'CognitiveServices',
    'MachineLearning': 'MachineLearning',
    'ML': 'MachineLearning',
    'BotService': 'BotService',
    'Bot': 'BotService',
    'Search': 'AzureCognitiveSearch',
    'AzureSearch': 'AzureCognitiveSearch',
    'CognitiveSearch': 'AzureCognitiveSearch',
    
    # Security aliases
    'KeyVault': 'KeyVault',
    'Vault': 'KeyVault',
    'Defender': 'MicrosoftDefenderForCloud',
    'SecurityCenter': 'MicrosoftDefenderForCloud',
    'Sentinel': 'Sentinel',
    
    # DevOps aliases
    'DevOps': 'AzureDevOps',
    'Pipelines': 'AzurePipelines',
    'Repos': 'AzureRepos',
    'Artifacts': 'AzureArtifacts',
    
    # General aliases
    'Internet': 'Globe',
    'Web': 'Globe',
    'User': 'User',
    'Users': 'Users',
    'Client': 'User',
    'ResourceGroup': 'ResourceGroup',
    'RG': 'ResourceGroup',
    'Subscription': 'Subscription',
}


def get_shape_info(resource_type: str) -> Tuple[str, str, str]:
    """
    Get shape information for a resource type.
    
    Returns: (display_name, category, style_string)
    
    Uses Draw.io's built-in Azure2 SVG icons for all resources.
    Supports aliases for common/intuitive names (e.g., 'SQL' -> 'AzureSQL').
    """
    # First, check if this is an alias and resolve it
    resolved_type = RESOURCE_TYPE_ALIASES.get(resource_type, resource_type)
    
    if resolved_type in AZURE_SHAPES:
        display_name, category, icon_path = AZURE_SHAPES[resolved_type]
        
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
