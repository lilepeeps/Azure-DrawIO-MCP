---
description: 'Instructions for generating structurally valid Azure Draw.io diagrams using the azure-drawio-mcp server'
applyTo: '**/*.drawio'
---

# Azure Draw.io Diagram Generation Instructions

These instructions help generate valid Azure architecture diagrams using the azure-drawio-mcp server.
The server handles XML generation internally, but understanding these patterns helps create better specifications.

## Quick Reference: Diagram Request Structure

When requesting a diagram from the azure-drawio-mcp server, provide:

```json
{
  "title": "My Azure Architecture",
  "resources": [
    {
      "id": "web",
      "resource_type": "AppService",
      "name": "Web App",
      "group": "compute",
      "rationale": "Hosts the web application"
    }
  ],
  "connections": [
    { "source": "web", "target": "db", "label": "SQL" }
  ],
  "groups": [
    { "id": "compute", "name": "Compute", "color": "#E6F3FF" }
  ],
  "use_infinite_canvas": true
}
```

## Best Practices for Diagram Specifications

### 1. Resource IDs

Use short, descriptive IDs that describe the resource's function:

**Good IDs:**
- `web-app`, `sql-db`, `storage`, `api-gateway`, `key-vault`

**Avoid:**
- `resource1`, `vm1`, `thing-a` (too generic)
- Long IDs with UUIDs (hard to read in connections)

### 2. Resource Types

Use common Azure resource type aliases. The server resolves these to official icons:

| Category | Types |
|----------|-------|
| Compute | `VM`, `AKS`, `AppService`, `Functions`, `ContainerApp` |
| Data | `SQL`, `Cosmos`, `MySQL`, `PostgreSQL`, `Redis` |
| Storage | `Blob`, `Files`, `Queue`, `Table`, `DataLake` |
| Network | `VNet`, `FrontDoor`, `AppGateway`, `LoadBalancer`, `DNS` |
| Security | `KeyVault`, `Entra`, `Firewall`, `NSG`, `WAF` |
| AI/ML | `OpenAI`, `CognitiveServices`, `MachineLearning`, `BotService` |
| Integration | `ServiceBus`, `EventHub`, `EventGrid`, `LogicApps`, `APIM` |

### 3. Groups for Organization

Groups create visual containers that organize related resources:

```json
{
  "groups": [
    { "id": "frontend", "name": "Frontend Tier", "color": "#E6F3FF" },
    { "id": "backend", "name": "Backend Services", "color": "#FFF3E0" },
    { "id": "data", "name": "Data Tier", "color": "#E8F5E9" }
  ]
}
```

**Group Colors:**
- Azure Blue: `#E6F3FF` (frontend, networking)
- Orange: `#FFF3E0` (compute, processing)
- Green: `#E8F5E9` (data, storage)
- Purple: `#F3E5F5` (security, identity)
- Gray: `#F5F5F5` (external, neutral)

### 4. Connections with Labels

Connections show data flow between resources:

```json
{
  "connections": [
    { "source": "gateway", "target": "webapp", "label": "HTTPS" },
    { "source": "webapp", "target": "sql", "label": "Data", "style": "solid" },
    { "source": "webapp", "target": "keyvault", "label": "Secrets", "style": "dashed" }
  ]
}
```

**Connection Styles:**
- `solid` - Primary data flows (default)
- `dashed` - Secondary or async connections
- `dotted` - Optional or management plane

### 5. Rationale for Legend

Include `rationale` on resources to populate the legend table:

```json
{
  "id": "sql",
  "resource_type": "SQL",
  "name": "Customer Database",
  "rationale": "Stores customer profiles and order history"
}
```

The legend shows: Number, Name, Type, and Rationale for each resource.

### 6. Canvas Options

**Infinite Canvas** (recommended for web docs):
```json
{ "use_infinite_canvas": true }
```
- No visible page boundaries
- Content scales naturally
- Better for embedding in documentation

**A4 Fixed Page** (for printing):
```json
{ "use_infinite_canvas": false }
```
- Shows A4 page boundaries
- Good for PDF export
- Predictable print layout

## Common Architecture Patterns

### Web Application (3-Tier)

```json
{
  "resources": [
    { "id": "users", "resource_type": "Users", "name": "End Users" },
    { "id": "fd", "resource_type": "FrontDoor", "name": "Azure Front Door", "group": "ingress" },
    { "id": "web", "resource_type": "AppService", "name": "Web App", "group": "compute" },
    { "id": "api", "resource_type": "Functions", "name": "API Functions", "group": "compute" },
    { "id": "sql", "resource_type": "SQL", "name": "Azure SQL", "group": "data" },
    { "id": "kv", "resource_type": "KeyVault", "name": "Key Vault", "group": "security" }
  ],
  "connections": [
    { "source": "users", "target": "fd" },
    { "source": "fd", "target": "web" },
    { "source": "web", "target": "api" },
    { "source": "api", "target": "sql", "label": "Data" },
    { "source": "api", "target": "kv", "label": "Secrets" }
  ],
  "groups": [
    { "id": "ingress", "name": "Ingress", "color": "#E6F3FF" },
    { "id": "compute", "name": "Application", "color": "#FFF3E0" },
    { "id": "data", "name": "Data", "color": "#E8F5E9" },
    { "id": "security", "name": "Security", "color": "#F3E5F5" }
  ]
}
```

### Microservices (Event-Driven)

```json
{
  "resources": [
    { "id": "api", "resource_type": "APIM", "name": "API Gateway" },
    { "id": "orders", "resource_type": "ContainerApp", "name": "Orders Service", "group": "services" },
    { "id": "inventory", "resource_type": "ContainerApp", "name": "Inventory Service", "group": "services" },
    { "id": "notify", "resource_type": "Functions", "name": "Notifications", "group": "services" },
    { "id": "bus", "resource_type": "ServiceBus", "name": "Service Bus", "group": "messaging" },
    { "id": "cosmos", "resource_type": "Cosmos", "name": "Cosmos DB", "group": "data" }
  ],
  "connections": [
    { "source": "api", "target": "orders" },
    { "source": "orders", "target": "bus", "label": "Events" },
    { "source": "bus", "target": "inventory", "style": "dashed" },
    { "source": "bus", "target": "notify", "style": "dashed" },
    { "source": "orders", "target": "cosmos" },
    { "source": "inventory", "target": "cosmos" }
  ]
}
```

## Validation

After generating a diagram, the server validates:

1. **Required root structure** - `id="0"` and `id="1"` cells present
2. **Unique IDs** - No duplicate resource IDs
3. **Valid references** - All connection sources/targets exist
4. **Valid parent references** - Grouped resources reference valid groups
5. **Geometry attributes** - All shapes have proper geometry

If validation fails, you'll receive detailed error messages explaining what to fix.

## Tips for Better Diagrams

1. **Start with groups** - Define your logical tiers before resources
2. **Use topology-aware layout** - Connections help the auto-layout place sources left, targets right
3. **Include rationale** - Makes the legend meaningful for stakeholders
4. **Keep it focused** - 10-15 resources per diagram is ideal
5. **Use infinite canvas for docs** - Better for web embedding without page boundaries

## References

- [Azure Architecture Icons](https://learn.microsoft.com/azure/architecture/icons/)
- [Draw.io Documentation](https://www.drawio.com/doc/)
- Based on learnings from [drawio-ninja](https://github.com/simonholdsworth/drawio-ninja)
