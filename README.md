# Azure Draw.io MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)]()
[![Draw.io](https://img.shields.io/badge/Draw.io-Editable-orange.svg)](https://www.drawio.com/)

Generate **editable** Azure architecture diagrams in Draw.io format using an MCP server.

> **What's an MCP Server?** Think of it as a plugin for AI assistants like GitHub Copilot or Claude. Once configured, you can simply ask "draw me an Azure architecture diagram" and it generates one for you.

> **Attribution**: This project is inspired by [dminkovski/azure-diagram-mcp](https://github.com/dminkovski/azure-diagram-mcp) which generates PNG diagrams using the Python `diagrams` package. This version outputs editable `.drawio` files instead.

## Table of Contents

- [Why Draw.io Instead of PNG?](#why-drawio-instead-of-png)
- [What It Does](#what-it-does)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
  - [Option A: Docker](#option-a-docker-recommended-for-multi-project-use-)
  - [Option B: Install from GitHub](#option-b-install-from-github-simplest-setup-)
  - [Option C: Local Python](#option-c-local-python-installation)
- [Usage Examples](#usage-examples)
- [MCP Tools](#mcp-tools)
- [Opening Generated Diagrams](#opening-generated-diagrams)
- [Example Prompts](#example-prompts-for-github-copilot)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

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
- Auto-layouts resources left-to-right (data sources on left, destinations on right)
- Groups resources into visual clusters (resource groups, VNets, subnets)
- Creates connections with labels and different line styles (solid, dashed, dotted)
- **Auto-opens diagrams** in VS Code after generation

### Fully Editable Output

Unlike PNG generators, **the diagram is just a starting point** — customize it however you like:

- **Drag icons** to reposition — connections auto-route
- **Resize groups** by dragging edges
- **Add labels** by double-clicking connections
- **Copy/paste** icons and groups between diagrams
- **Export** to PNG, SVG, or PDF when done

### Example Output

![Example AKS Architecture Diagram](docs/example-aks-architecture.png)

*Generated from a simple prompt: "AKS cluster with Application Gateway, Container Registry, Key Vault, and SQL Database"*

## Requirements

**At a Glance:** Python 3.10+, VS Code with the Draw.io extension, and one of: Docker OR the `uv` package manager.

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

| Option | Best For | What You Need |
|--------|----------|---------------|
| **A: Docker** | Multiple projects, consistent environment | Docker Desktop |
| **B: GitHub Install** | Quickest single setup | Python + `uv` package manager |
| **C: Local Python** | Development/contributions | Python + pip |

> **🤔 Not sure?** Use **Option A (Docker)** if you have Docker installed, or **Option B** if you don't. Option C is mainly for developers who want to modify this project.

> **💡 Tip:** This project includes a [dev container](.devcontainer/devcontainer.json) for instant setup - just open in VS Code and select "Reopen in Container".

> **⚠️ Configuration Format Note:** VS Code uses `servers` in `.vscode/mcp.json`, while Claude Desktop uses `mcpServers` in `claude_desktop_config.json`. Configuration examples for both are provided below.
>
> **📄 VS Code Sample:** Copy [`.vscode/mcp.json.sample`](.vscode/mcp.json.sample) to `.vscode/mcp.json` in your project and uncomment your preferred option.

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

**3. Configure MCP Client:**

<details>
<summary><strong>VS Code (.vscode/mcp.json)</strong></summary>

```json
{
  "servers": {
    "azure-drawio": {
      "type": "stdio",
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

</details>

<details>
<summary><strong>Claude Desktop (claude_desktop_config.json)</strong></summary>

```json
{
  "mcpServers": {
    "azure-drawio": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "/path/to/your/workspace:/workspace",
        "-e", "WORKSPACE_MOUNT=/workspace",
        "azure-drawio-mcp:latest"
      ]
    }
  }
}
```

</details>

> **Note**: When using Docker, the server automatically translates host paths to the container mount point at `/workspace`.

**Benefits:**
- No Python environment management needed
- Works consistently across all your projects
- Easy to update: just rebuild the image

---

### Option B: Install from GitHub (Simplest Setup) ⚡

**1. Install Prerequisites:**
- Python 3.10+
- `uv` package manager (a fast Python tool runner): `pip install uv` or `winget install astral-sh.uv`
- VS Code Draw.io Extension: `code --install-extension hediet.vscode-drawio`

**2. Configure MCP Client:**

<details>
<summary><strong>VS Code (.vscode/mcp.json)</strong></summary>

```json
{
  "servers": {
    "azure-drawio": {
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

</details>

<details>
<summary><strong>Claude Desktop (claude_desktop_config.json)</strong></summary>

```json
{
  "mcpServers": {
    "azure-drawio": {
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

</details>

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

<details>
<summary><strong>VS Code (.vscode/mcp.json)</strong></summary>

```json
{
  "servers": {
    "azure-drawio": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "azure_drawio_mcp_server.server"],
      "cwd": "/path/to/Azure-DrawIO-MCP"
    }
  }
}
```

</details>

<details>
<summary><strong>Claude Desktop (claude_desktop_config.json)</strong></summary>

```json
{
  "mcpServers": {
    "azure-drawio": {
      "command": "python",
      "args": ["-m", "azure_drawio_mcp_server.server"],
      "cwd": "/path/to/Azure-DrawIO-MCP"
    }
  }
}
```

</details>

---

### Verify Installation

After configuration, test the MCP server with the following prompt:

```
Use #azure-draw.io-mcp-server to generate an Azure diagram with a Function App, Storage Account, and Cosmos DB
```

The diagram should be created in your workspace's `diagrams/` folder and open in VS Code.

---

## Usage Examples

This MCP server supports multiple ways to generate Azure architecture diagrams:

### 🎯 Method 1: Natural Language Prompts

In VS Code with GitHub Copilot, describe what you want:

```
Generate an Azure architecture diagram showing an AKS cluster with Application Gateway, 
Container Registry, Key Vault, and Azure SQL Database
```

The AI will interpret your request and call the MCP server with the appropriate resources.

### 📂 Method 2: Scan Existing Repository

Already have Azure infrastructure in your project (Bicep, Terraform, ARM templates)? Use the included prompt file to help Copilot discover your resources:

**How to use it:**
1. Open GitHub Copilot chat in VS Code
2. Click the 📎 attachment icon
3. Select **Prompts → generate-architecture**
4. Ask: *"Analyze my infrastructure code and generate a diagram"*

The prompt file (`.github/prompts/generate-architecture.prompt.md`) tells Copilot what to look for and how to call the diagram generator.

> **💡 Why a prompt file?** GitHub Copilot already understands your code semantically — the prompt file just guides it to focus on Azure resources and call the right MCP tools.

### 📝 Method 3: Structured JSON Specification

For precise control, provide a full specification:

```json
{
  "title": "E-Commerce Platform",
  "resources": [
    {"id": "fd", "resource_type": "FrontDoor", "name": "Front Door", "group": "network"},
    {"id": "app", "resource_type": "WebApp", "name": "Web App", "group": "compute"},
    {"id": "sql", "resource_type": "SQL", "name": "SQL Database", "group": "data"}
  ],
  "groups": [
    {"id": "network", "name": "Network"},
    {"id": "compute", "name": "Compute"},
    {"id": "data", "name": "Data"}
  ],
  "connections": [
    {"source": "fd", "target": "app"},
    {"source": "app", "target": "sql"}
  ]
}
```

---

## Tips for Better Diagrams

The MCP server validates your input and provides guidance:

| Aspect | Recommendation |
|--------|----------------|
| **Resource Types** | Use friendly aliases: `SQL`, `Cosmos`, `AKS`, `Functions`, `WebApp` |
| **Groups** | Organize resources into logical groups for better layout |
| **Connections** | Define data flow between resources — helps auto-layout |
| **Naming** | Use clear, short names — they appear as labels |
| **Size** | Keep diagrams under 15-20 resources for clarity |

### Common Resource Type Aliases

| Type | Alias Options |
|------|---------------|
| Azure SQL | `SQL`, `SQLDatabase`, `SQLDB`, `AzureSQL` |
| Cosmos DB | `Cosmos`, `CosmosDB`, `AzureCosmosDB` |
| Kubernetes | `AKS`, `Kubernetes`, `K8s`, `KubernetesServices` |
| Functions | `Functions`, `Function`, `FunctionApp`, `AzureFunctions` |
| App Service | `WebApp`, `App`, `AppService` |
| Storage | `BlobStorage`, `Blob`, `FileStorage`, `Files`, `Storage` |
| Key Vault | `KeyVault`, `Vault` |
| Redis | `Redis`, `RedisCache`, `Cache`, `CacheRedis` |

---

## Editing Generated Diagrams

Generated diagrams include instruction text at the top. Here's how to customize:

1. **Move Resources**: Click and drag any icon — connections auto-route
2. **Resize Groups**: Drag group edges to make room
3. **Move Groups**: Click the group header to drag the entire group
4. **Add Labels**: Double-click a connection to add descriptive text
5. **Reroute Arrows**: Click a connection and drag the waypoints
6. **Copy/Paste**: Ctrl+C/V works for icons and groups
7. **Add Resources**: Drag Azure icons from the shapes panel

The layout is designed for **A4 landscape** export.

---

## MCP Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `generate_diagram` | Create diagram from structured spec | Full control over resources, groups, connections |
| `list_azure_shapes` | Browse available Azure icons | Find the right `resource_type` value |
| `get_diagram_examples` | Get template specifications | Starting point for common architectures |

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

---

### Optional: `scan_workspace`

> **Note:** For GitHub Copilot users, the [prompt file approach](#-method-2-scan-existing-repository-prompt-file) is recommended. Copilot's semantic understanding is more accurate than regex-based scanning.

For non-Copilot MCP clients (Claude Desktop standalone, etc.), `scan_workspace` provides basic resource discovery:

**Parameters:**
- `workspace_dir` (required): Path to scan
- `generate_diagram`: Auto-generate diagram (default: true)
- `filename`: Output filename
- `open_in_vscode`: Open in VS Code after generation

**Scans for:** Bicep (`*.bicep`), Terraform (`*.tf`), ARM templates, Azure SDK usage patterns.

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
├── .github/
│   └── prompts/
│       └── generate-architecture.prompt.md  # Prompt for codebase scanning
├── azure_drawio_mcp_server/
│   ├── __init__.py           # Package initialization
│   ├── server.py             # MCP server that handles AI assistant requests
│   ├── drawio_generator.py   # Creates .drawio files using drawpyo library
│   ├── azure_shapes.py       # Azure resource type mappings and styles
│   ├── scanner.py            # Workspace scanner (optional)
│   └── models.py             # Data models for requests/responses
├── diagrams/                 # Generated diagram output directory
├── .dockerignore             # Docker build exclusions
├── Dockerfile                # Container image definition
├── pyproject.toml            # Python package metadata and dependencies
├── requirements.txt          # Python dependencies (pip)
├── README.md                 # This file
└── LICENSE                   # MIT License
```

## Dependencies

This project uses three Python libraries (installed automatically):

- **drawpyo**: Creates Draw.io files programmatically
- **mcp[cli]**: Enables communication with AI assistants
- **pydantic**: Handles data validation

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
