---
description: "Scan codebase and generate Azure architecture diagram"
tools: ['vscode', 'execute', 'read', 'edit', 'search', 'web', 'azure-draw.io-mcp-server/*', 'agent', 'todo']
---

# Generate Azure Architecture Diagram

Analyze the current workspace to identify Azure resources and generate an architecture diagram.

## Discovery Phase

Scan the codebase for Azure resources in:

1. **Infrastructure as Code**
   - Bicep files (`*.bicep`) - look for `resource` declarations
   - Terraform files (`*.tf`) - look for `azurerm_*` resources
   - ARM templates (`*.json`) - look for `Microsoft.*` resource types

2. **Application Code**
   - Connection strings referencing Azure services
   - Azure SDK client instantiations
   - Environment variables with Azure service URLs

3. **Configuration Files**
   - `appsettings.json`, `.env`, `local.settings.json`
   - Kubernetes manifests referencing Azure resources
   - Docker compose files with Azure integrations

## Diagram Generation

After discovering resources, call the `generate_diagram` tool with:

- **Resources**: Each Azure service found, with a clear name and appropriate `resource_type`
- **Groups**: Organize by logical layer (Network, Compute, Data, Security, etc.)
- **Connections**: Infer data flow from how resources reference each other
- **Rationale**: Brief explanation of each resource's purpose in the architecture

## Resource Type Mapping

Use these friendly aliases for common services:

| Service | resource_type |
|---------|---------------|
| Azure SQL | `SQL` |
| Cosmos DB | `Cosmos` |
| AKS | `AKS` |
| Functions | `Functions` |
| App Service | `WebApp` |
| Storage Account | `StorageAccount` |
| Key Vault | `KeyVault` |
| Application Gateway | `ApplicationGateway` |
| Event Hub | `EventHub` |
| Service Bus | `ServiceBus` |

## Output

Generate the diagram with:
- `show_legend: true` - include rationale for each resource
- `show_instructions: true` - help users customize the layout
- `open_in_vscode: true` - open immediately for editing
