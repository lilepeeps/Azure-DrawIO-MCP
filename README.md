# Azure Draw.io MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)]()
[![Draw.io](https://img.shields.io/badge/Draw.io-Editable-orange.svg)](https://www.drawio.com/)

Generate **editable** Azure architecture diagrams in Draw.io format using an MCP server.

> **Attribution**: This project is inspired by [dminkovski/azure-diagram-mcp](https://github.com/dminkovski/azure-diagram-mcp) which generates PNG diagrams using the Python `diagrams` package. This version outputs editable `.drawio` files instead.

## Why Draw.io Instead of PNG?

| Feature | PNG (Original) | Draw.io (This Project) |
|---------|---------------|------------------------|
| **Editable** | ❌ Not editable | ✅ Fully editable |
| **Version Control** | ⚠️ Binary diffs | ✅ XML text diffs |
| **VS Code Integration** | View only | ✅ Edit in VS Code |
| **Export Options** | PNG only | ✅ PNG, SVG, PDF |
| **Dependencies** | Requires Graphviz | ✅ Pure Python |
| **Adjust Layout** | ❌ Regenerate | ✅ Drag and drop |
| **Azure Icons** | ✅ Built-in | ✅ Azure2 SVG Library |

## What It Does

- Generates Azure architecture diagrams as `.drawio` files
- Uses **official Azure icons** from Draw.io's Azure2 SVG library
- Supports 100+ Azure resource types (VMs, App Services, AKS, SQL, etc.)
- Auto-layouts resources with optional manual positioning
- Groups resources into styled clusters (resource groups, VNets, subnets)
- Creates connections with labels and different line styles (solid, dashed, dotted)
- **Auto-opens diagrams** in VS Code after generation

## Requirements

### Required

| Component | Version | Installation |
|-----------|---------|--------------|
| **Python** | 3.10+ | `winget install Python.Python.3.12` |
| **pip packages** | See requirements.txt | `pip install -r requirements.txt` |

### Recommended (for VS Code integration)

| Component | Purpose | Installation |
|-----------|---------|--------------|
| **VS Code** | Editor | [Download](https://code.visualstudio.com/) |
| **Draw.io Extension** | Edit .drawio files in VS Code | `code --install-extension hediet.vscode-drawio` |

## Quick Start

Choose one of three installation methods:

> **💡 Tip:** This project includes a [dev container](.devcontainer/devcontainer.json) for instant setup - just open in VS Code and select "Reopen in Container".

### Option A: Docker (Recommended for Multi-Project Use) 🐳

**1. Install Prerequisites:**
- Docker Desktop ([Windows/Mac](https://www.docker.com/products/docker-desktop/) | Linux: `sudo apt install docker.io`)
- VS Code Draw.io Extension: `code --install-extension hediet.vscode-drawio`

**2. Clone and Build:**

```bash
git clone https://github.com/lilepeeps/Azure-DrawIO-MCP.git
cd Azure-DrawIO-MCP
docker build -t azure-drawio-mcp:latest .
```

**3. Configure MCP Client** (e.g., Claude Desktop, VS Code):

```json
{
  "mcpServers": {
    "azure-drawio": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "${workspaceFolder}:/workspace",
        "-e", "WORKSPACE_MOUNT=/workspace",
        "azure-drawio-mcp:latest"
      ]
    }
  }
}
```

> **Note**: When using Docker, the server automatically translates host paths to the container mount point at `/workspace`.

**Benefits:**
- No Python environment management needed
- Works consistently across all your projects
- Easy to update: just rebuild the image

---

### Option B: Install from GitHub (No Clone Required)

**1. Install Prerequisites:**
- Python 3.10+
- `uv` package manager: `pip install uv` or `winget install astral-sh.uv`
- VS Code Draw.io Extension: `code --install-extension hediet.vscode-drawio`

**2. Configure MCP Client:**

```json
{
  "mcpServers": {
    "Azure Draw.io MCP Server": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from", 
        "git+https://github.com/lilepeeps/Azure-DrawIO-MCP.git",
        "azure-drawio-mcp"
      ]
    }
  }
}
```

---

### Option C: Local Python Installation

**1. Install Prerequisites:**

Python 3.10+ is required:

```bash
# Windows
winget install Python.Python.3.12

# macOS
brew install python@3.12

# Linux (Ubuntu/Debian)
sudo apt install python3.12 python3.12-venv
```

VS Code Draw.io Extension:

```bash
code --install-extension hediet.vscode-drawio
```

**2. Clone and Install:**

```bash
git clone https://github.com/lilepeeps/Azure-DrawIO-MCP.git
cd Azure-DrawIO-MCP

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**3. Configure MCP Client:**

```json
{
  "mcpServers": {
    "Azure Draw.io MCP Server": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "azure_drawio_mcp_server.server"],
      "cwd": "/path/to/Azure-DrawIO-MCP"
    }
  }
}
```

---

### Verify Installation

After configuration, test the MCP server with the following prompt:

```
Use #azure-draw.io-mcp-server to generate an Azure diagram with a Function App, Storage Account, and Cosmos DB
```

The diagram should be created in your workspace's `diagrams/` folder and open in VS Code.

---

## Usage Examples

In VS Code with GitHub Copilot, use prompts like:

```
Generate an Azure architecture diagram showing an AKS cluster with Application Gateway, 
Container Registry, Key Vault, and Azure SQL Database
```

Or scan your existing codebase:

```
Scan my workspace and generate an Azure architecture diagram based on my infrastructure code
```

## MCP Tools

### `scan_workspace` ⭐ NEW

Automatically scans your codebase to discover Azure resources and generate a diagram.

**Scans for:**
- Bicep files (`*.bicep`)
- Terraform files (`*.tf`)
- ARM templates (`*.json` with ARM schema)
- Azure SDK usage (`*.cs`, `*.py`, `*.js`, `*.ts`)

**Parameters:**
- `workspace_dir` (required): Path to scan
- `generate_diagram`: Auto-generate diagram (default: true)
- `filename`: Output filename
- `open_in_vscode`: Open in VS Code after generation

**Example prompt:**
```
Scan my project at C:/Projects/my-azure-app and create an architecture diagram
```

### `generate_diagram`

Creates a Draw.io diagram from a structured specification.

**Parameters:**
- `title` (required): Diagram title
- `resources` (required): List of Azure resources
  - Each resource can include an optional `rationale` field for the legend
- `connections`: List of connections between resources
- `groups`: Optional resource groups/clusters
- `workspace_dir`: Where to save the diagram
- `filename`: Output filename (without .drawio extension)
- `open_in_vscode`: Open the diagram in VS Code after generation (default: false)
- `show_legend`: Show a numbered legend table at the bottom (default: true)

**Example:**
```json
{
  "title": "Web Application Architecture",
  "resources": [
    {"id": "fd", "resource_type": "FrontDoor", "name": "Azure Front Door", "rationale": "Global load balancing and CDN"},
    {"id": "app", "resource_type": "AppService", "name": "Web App", "rationale": "Hosts the React frontend"},
    {"id": "sql", "resource_type": "SQLDatabase", "name": "Azure SQL", "rationale": "Managed relational database"}
  ],
  "connections": [
    {"source": "fd", "target": "app"},
    {"source": "app", "target": "sql"}
  ],
  "open_in_vscode": true,
  "show_legend": true
}
```

### `list_azure_shapes`

Lists all available Azure resource types organized by category.

**Categories:**
- `compute`: VM, AKS, AppService, FunctionApp, ContainerInstances
- `network`: VNet, LoadBalancer, ApplicationGateway, Firewall, VPNGateway
- `storage`: StorageAccount, BlobStorage, DataLake, ManagedDisk
- `database`: SQLDatabase, CosmosDB, Redis, MySQL, PostgreSQL
- `web`: APIM, SignalR, StaticWebApp
- `security`: KeyVault, EntraID, Sentinel, SecurityCenter
- `integration`: ServiceBus, EventHub, EventGrid, LogicApp, DataFactory
- `ai`: AzureOpenAI, CognitiveServices, MachineLearning, AISearch
- `analytics`: Synapse, Databricks, StreamAnalytics, PowerBI
- `devops`: DevOps, Monitor, LogAnalytics, AppInsights
- `iot`: IoTHub, IoTCentral, DigitalTwins
- `general`: User, Client, Browser, OnPremise, Internet

### `get_diagram_examples`

Returns example diagram specifications you can use as templates.

**Types:** `azure`, `network`, `compute`, `data`, `integration`, `security`, `all`

## Opening Generated Diagrams

### Automatic Opening (Recommended)

Set `open_in_vscode: true` when generating diagrams and they'll open automatically in VS Code. Requires:
- VS Code installed with `code` command in PATH
- Draw.io extension: `hediet.vscode-drawio`

### VS Code Manual

1. Install the Draw.io extension: `hediet.vscode-drawio`
2. Open the generated `.drawio` file
3. Edit directly in VS Code!

### Draw.io Desktop/Web

1. Download Draw.io: https://www.drawio.com/
2. Open → Select your `.drawio` file
3. Edit and export as needed

## Resource Type Reference

Use these `resource_type` values when defining resources:

```
Compute:     VM, VMSS, AppService, FunctionApp, AKS, ContainerInstances, ACR
Network:     VNet, Subnet, LoadBalancer, ApplicationGateway, FrontDoor, Firewall, VPNGateway
Storage:     StorageAccount, BlobStorage, FileStorage, DataLake, ManagedDisk
Database:    SQLDatabase, CosmosDB, Redis, MySQL, PostgreSQL, Synapse
Web:         APIM, SignalR, StaticWebApp
Security:    KeyVault, EntraID, ManagedIdentity, Sentinel, SecurityCenter
Integration: ServiceBus, EventHub, EventGrid, LogicApp, DataFactory
AI/ML:       AzureOpenAI, CognitiveServices, MachineLearning, AISearch, BotService
Analytics:   Synapse, Databricks, StreamAnalytics, HDInsight, PowerBI
DevOps:      DevOps, Monitor, LogAnalytics, AppInsights, Automation
IoT:         IoTHub, IoTCentral, DigitalTwins
General:     User, Client, Browser, Mobile, OnPremise, Internet, Cloud
```

## Example Prompts for GitHub Copilot

```
Generate a hub-spoke network architecture with Azure Firewall in the hub 
and AKS clusters in the spokes

Create a serverless event-driven architecture using Event Hubs, 
Azure Functions, and Cosmos DB

Design a zero-trust architecture with Entra ID, Application Gateway with WAF, 
Private Endpoints, and Microsoft Sentinel for monitoring
```

## Project Structure

```
azure-drawio-mcp/
├── azure_drawio_mcp_server/
│   ├── __init__.py           # Package initialization
│   ├── server.py             # FastMCP server with tool definitions
│   ├── drawio_generator.py   # Draw.io file generation using drawpyo
│   ├── azure_shapes.py       # Azure resource type mappings and styles
│   ├── scanner.py            # Workspace scanner for auto-discovery
│   └── models.py             # Pydantic request/response models
├── diagrams/                 # Generated diagram output directory
├── .dockerignore             # Docker build exclusions
├── Dockerfile                # Container image definition
├── pyproject.toml            # Python package metadata and dependencies
├── requirements.txt          # Python dependencies (pip)
├── README.md                 # This file
└── LICENSE                   # MIT License
```

## Dependencies

- **drawpyo**: Python library for generating Draw.io files
- **mcp[cli]**: Model Context Protocol SDK
- **pydantic**: Data validation and serialization

No Graphviz installation required! 🎉

## Troubleshooting

### Diagram not created?
- Check that `workspace_dir` is a valid, writable path
- Look for errors in the MCP server output

### Can't open .drawio file in VS Code?
- Install the Draw.io extension: `code --install-extension hediet.vscode-drawio`
- Restart VS Code after installation

### MCP server not responding?
- Verify Python path in your MCP configuration
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Ensure the `cwd` path points to the project root

## License

MIT License - See [LICENSE](LICENSE) file.

## Acknowledgments

- **Original Inspiration**: [dminkovski/azure-diagram-mcp](https://github.com/dminkovski/azure-diagram-mcp) - PNG diagram generation using the diagrams package
- **Draw.io Generation**: [MerrimanInd/drawpyo](https://github.com/MerrimanInd/drawpyo) - Python library for creating Draw.io files
- **VS Code Integration**: [hediet.vscode-drawio](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) - Draw.io editor for VS Code
