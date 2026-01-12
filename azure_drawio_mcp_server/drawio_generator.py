# Copyright (c) 2026. Inspired by dminkovski/azure-diagram-mcp
"""Draw.io diagram generation using drawpyo library."""

import os
import subprocess
import sys
import uuid
import tempfile
import logging
from typing import Dict, List, Optional, Tuple

import drawpyo
from drawpyo.diagram import objects as drawpyo_objects

from azure_drawio_mcp_server.models import (
    AzureResource,
    Connection,
    ResourceGroup,
    DiagramRequest,
    DiagramResponse,
)
from azure_drawio_mcp_server.azure_shapes import (
    get_shape_info,
    get_group_style,
    get_edge_style,
    DEFAULT_WIDTH,
    DEFAULT_HEIGHT,
    ICON_SIZE,
    AZURE_COLORS,
    AZURE_SHAPES,
)

logger = logging.getLogger(__name__)

# Grid layout constants - increased for better spacing
GRID_SPACING_X = 300
GRID_SPACING_Y = 220
START_X = 80
START_Y = 100
GROUP_PADDING = 100

# Legend table styling
LEGEND_HEADER_STYLE = (
    "swimlane;fontStyle=1;childLayout=stackLayout;horizontal=1;startSize=30;"
    "horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;"
    "collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#0078D4;"
    "fontColor=#ffffff;strokeColor=#0078D4;rounded=1;"
)
LEGEND_ROW_STYLE = (
    "text;strokeColor=#0078D4;fillColor=#ffffff;align=left;verticalAlign=middle;"
    "spacingLeft=10;spacingRight=10;overflow=hidden;points=[[0,0.5],[1,0.5]];"
    "portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;fontSize=11;"
)
LEGEND_ROW_ALT_STYLE = (
    "text;strokeColor=#0078D4;fillColor=#F0F8FF;align=left;verticalAlign=middle;"
    "spacingLeft=10;spacingRight=10;overflow=hidden;points=[[0,0.5],[1,0.5]];"
    "portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;fontSize=11;"
)


def _open_in_vscode(file_path: str) -> bool:
    """
    Open a file in VS Code using the 'code' command.
    
    Returns True if the command was executed successfully, False otherwise.
    Requires VS Code to be installed and the 'code' command in PATH.
    For Draw.io files, requires the hediet.vscode-drawio extension.
    """
    try:
        # Use 'code' command which works on Windows, macOS, and Linux
        if sys.platform == 'win32':
            # On Windows, use shell=True to find 'code' in PATH
            subprocess.Popen(
                ['code', file_path],
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            # On Unix-like systems
            subprocess.Popen(
                ['code', file_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        return True
    except FileNotFoundError:
        logger.warning("VS Code 'code' command not found in PATH")
        return False
    except Exception as e:
        logger.warning(f"Failed to open file in VS Code: {e}")
        return False


def _calculate_layout(
    resources: List[AzureResource],
    groups: List[ResourceGroup]
) -> Tuple[Dict[str, Tuple[int, int]], Dict[str, Tuple[int, int, int, int]]]:
    """
    Calculate positions for resources and bounds for groups.
    
    Returns:
        - positions: Dict mapping resource ID to (x, y) position
          For ungrouped resources: absolute position on page
          For grouped resources: position RELATIVE to group origin (0,0 = top-left of group)
        - group_bounds: Dict mapping group ID to (x, y, width, height)
    """
    positions: Dict[str, Tuple[int, int]] = {}
    group_bounds: Dict[str, Tuple[int, int, int, int]] = {}
    
    # Separate resources by group
    grouped: Dict[Optional[str], List[AzureResource]] = {}
    for resource in resources:
        group_id = resource.group
        if group_id not in grouped:
            grouped[group_id] = []
        grouped[group_id].append(resource)
    
    current_y = START_Y
    
    # Position ungrouped resources first (at the top)
    if None in grouped:
        ungrouped = grouped[None]
        for i, resource in enumerate(ungrouped):
            if resource.x is not None and resource.y is not None:
                positions[resource.id] = (resource.x, resource.y)
            else:
                x = START_X + (i % 5) * GRID_SPACING_X
                y = current_y + (i // 5) * GRID_SPACING_Y
                positions[resource.id] = (x, y)
        
        # Move y down for grouped resources
        rows_used = (len(ungrouped) + 4) // 5
        current_y += rows_used * GRID_SPACING_Y + GROUP_PADDING * 2
    
    # Position groups and their resources
    group_x = START_X
    group_row_height = 0
    groups_per_row = 2  # Place 2 groups side by side
    
    # Sizing constants for content
    TITLE_HEIGHT = 40       # Height for swimlane title bar
    CONTENT_PADDING = 30    # Padding inside group around resources
    ICON_WIDTH = ICON_SIZE  # Width of each icon
    ICON_HEIGHT = ICON_SIZE + 30  # Icon + label below
    
    for group_idx, group in enumerate(groups):
        if group.id in grouped:
            group_resources = grouped[group.id]
            num_resources = len(group_resources)
            
            # Layout resources in a grid inside the group
            cols = min(3, num_resources)  # Max 3 columns
            rows = (num_resources + cols - 1) // cols
            
            # Calculate group dimensions to fully contain resources
            content_width = cols * GRID_SPACING_X
            content_height = rows * GRID_SPACING_Y
            
            group_width = CONTENT_PADDING * 2 + content_width
            group_height = TITLE_HEIGHT + CONTENT_PADDING * 2 + content_height
            
            # Ensure minimum size
            group_width = max(300, group_width)
            group_height = max(150, group_height)
            
            # Position each resource RELATIVE to the group's origin (0,0)
            # Resources start after title bar and padding
            for i, resource in enumerate(group_resources):
                if resource.x is not None and resource.y is not None:
                    # User specified position (relative to group)
                    positions[resource.id] = (resource.x, resource.y)
                else:
                    # Auto-layout within group
                    col = i % cols
                    row = i // cols
                    # Position relative to group origin
                    rel_x = CONTENT_PADDING + col * GRID_SPACING_X
                    rel_y = TITLE_HEIGHT + CONTENT_PADDING + row * GRID_SPACING_Y
                    positions[resource.id] = (rel_x, rel_y)
            
            # Store group bounds (position and size)
            group_bounds[group.id] = (group_x, current_y, group_width, group_height)
            
            # Track tallest group in this row
            group_row_height = max(group_row_height, group_height)
            
            # Move to next group position
            if (group_idx + 1) % groups_per_row == 0:
                # New row of groups
                group_x = START_X
                current_y += group_row_height + GROUP_PADDING * 2
                group_row_height = 0
            else:
                # Same row, move right
                group_x += group_width + GROUP_PADDING * 2
    
    return positions, group_bounds


def _calculate_diagram_bottom(
    positions: Dict[str, Tuple[int, int]],
    group_bounds: Dict[str, Tuple[int, int, int, int]],
) -> int:
    """Calculate the bottom-most Y coordinate of the diagram content."""
    max_y = START_Y
    
    # Check ungrouped resource positions
    for x, y in positions.values():
        max_y = max(max_y, y + DEFAULT_HEIGHT + 50)  # Resource height + label
    
    # Check group bottoms
    for x, y, w, h in group_bounds.values():
        max_y = max(max_y, y + h)
    
    return max_y


def _create_legend(
    page,
    resources: List[AzureResource],
    x: int,
    y: int,
) -> None:
    """
    Create a legend table at the specified position.
    
    The legend shows numbered resources with their name, type, and rationale.
    Each row is manually positioned (not using swimlane stacking which doesn't work).
    """
    # Calculate column widths
    COL_NUM = 50
    COL_NAME = 200
    COL_TYPE = 180
    COL_RATIONALE = 350
    TABLE_WIDTH = COL_NUM + COL_NAME + COL_TYPE + COL_RATIONALE
    ROW_HEIGHT = 28
    HEADER_HEIGHT = 36
    
    # Calculate total height
    table_height = HEADER_HEIGHT + (len(resources) + 1) * ROW_HEIGHT
    
    # Create table title/header bar
    title_bar = drawpyo_objects.Object(page=page)
    title_bar.value = "📋 Architecture Legend"
    title_bar.position = (x, y)
    title_bar.width = TABLE_WIDTH
    title_bar.height = HEADER_HEIGHT
    title_bar.apply_style_string(
        "rounded=1;whiteSpace=wrap;html=1;fillColor=#0078D4;fontColor=#ffffff;"
        "fontStyle=1;fontSize=14;align=center;verticalAlign=middle;strokeColor=#005a9e;"
    )
    
    current_y = y + HEADER_HEIGHT
    
    # Create column header row
    header_row = drawpyo_objects.Object(page=page)
    header_row.value = (
        f"<table style='width:100%;border-collapse:collapse;'>"
        f"<tr style='font-weight:bold;'>"
        f"<td style='width:{COL_NUM}px;padding:4px;'>#</td>"
        f"<td style='width:{COL_NAME}px;padding:4px;'>Name</td>"
        f"<td style='width:{COL_TYPE}px;padding:4px;'>Type</td>"
        f"<td style='width:{COL_RATIONALE}px;padding:4px;'>Rationale</td>"
        f"</tr></table>"
    )
    header_row.position = (x, current_y)
    header_row.width = TABLE_WIDTH
    header_row.height = ROW_HEIGHT
    header_row.apply_style_string(
        "text;strokeColor=#0078D4;fillColor=#E6F3FF;align=left;verticalAlign=middle;"
        "overflow=hidden;whiteSpace=wrap;html=1;fontStyle=1;fontSize=11;"
    )
    current_y += ROW_HEIGHT
    
    # Create data rows - each positioned manually
    for idx, resource in enumerate(resources, 1):
        row = drawpyo_objects.Object(page=page)
        
        # Get display name for the type
        display_type, _, _ = get_shape_info(resource.resource_type)
        rationale = resource.rationale or "—"
        
        row.value = (
            f"<table style='width:100%;border-collapse:collapse;'>"
            f"<tr>"
            f"<td style='width:{COL_NUM}px;padding:4px;font-weight:bold;color:#0078D4;'>{idx}</td>"
            f"<td style='width:{COL_NAME}px;padding:4px;'>{resource.name}</td>"
            f"<td style='width:{COL_TYPE}px;padding:4px;color:#666;'>{display_type}</td>"
            f"<td style='width:{COL_RATIONALE}px;padding:4px;'>{rationale}</td>"
            f"</tr></table>"
        )
        row.position = (x, current_y)
        row.width = TABLE_WIDTH
        row.height = ROW_HEIGHT
        
        # Alternate row colors
        if idx % 2 == 0:
            row.apply_style_string(LEGEND_ROW_ALT_STYLE)
        else:
            row.apply_style_string(LEGEND_ROW_STYLE)
        
        current_y += ROW_HEIGHT


async def generate_drawio_diagram(
    request: DiagramRequest,
) -> DiagramResponse:
    """
    Generate a Draw.io diagram from the request specification.
    
    This creates a .drawio file that can be opened and edited in:
    - Draw.io desktop application
    - VS Code with Draw.io extension (hediet.vscode-drawio)
    - draw.io web application
    """
    try:
        # Determine output path
        if request.filename:
            filename = request.filename
            if not filename.endswith('.drawio'):
                filename = f"{filename}.drawio"
        else:
            filename = f"azure_diagram_{uuid.uuid4().hex[:8]}.drawio"
        
        # Determine output directory
        if request.workspace_dir and os.path.isdir(request.workspace_dir):
            # Check if workspace_dir already contains 'diagrams'
            if 'diagrams' in request.workspace_dir.lower():
                output_dir = request.workspace_dir
            else:
                output_dir = os.path.join(request.workspace_dir, 'diagrams')
        else:
            output_dir = os.path.join(tempfile.gettempdir(), 'azure-drawio-diagrams')
        
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)
        
        # Create Draw.io file and page
        file = drawpyo.File()
        file.file_path = output_dir
        file.file_name = filename
        
        page = drawpyo.Page(file=file)
        page.name = request.title
        
        # Calculate layout for all resources and groups
        positions, group_bounds = _calculate_layout(request.resources, request.groups)
        
        # Track created objects for edge connections
        objects: Dict[str, drawpyo_objects.Object] = {}
        
        # Create groups/clusters first (as container objects)
        group_objects: Dict[str, drawpyo_objects.Object] = {}
        for group in request.groups:
            if group.id not in group_bounds:
                continue  # Skip groups with no resources
            
            x, y, width, height = group_bounds[group.id]
            
            group_obj = drawpyo_objects.Object(page=page)
            group_obj.value = group.name
            group_obj.position = (x, y)
            # Set width and height directly (size tuple setter doesn't work in drawpyo)
            group_obj.width = width
            group_obj.height = height
            
            # Apply group style
            color = group.color or '#E6F3FF'
            group_obj.apply_style_string(get_group_style(color))
            
            group_objects[group.id] = group_obj
        
        # Build resource index map for numbering (matches legend order)
        resource_index = {res.id: idx + 1 for idx, res in enumerate(request.resources)}
        
        # Create resource shapes - nest inside groups when applicable
        for resource in request.resources:
            display_name, category, style = get_shape_info(resource.resource_type)
            
            # Determine if this resource belongs to a group
            parent_group = None
            if resource.group and resource.group in group_objects:
                parent_group = group_objects[resource.group]
            
            # Create the object - either on page or as child of group
            obj = drawpyo_objects.Object(page=page)
            
            # Get the resource number for labeling
            res_num = resource_index.get(resource.id, 0)
            
            # Check if this resource type uses an icon (has an icon path)
            has_icon = (
                resource.resource_type in AZURE_SHAPES 
                and AZURE_SHAPES[resource.resource_type][2] is not None
            )
            
            if has_icon:
                # For icons, show number and name below the icon
                obj.value = f"<b style='color:#0078D4;'>[{res_num}]</b> {resource.name}"
                obj.size = (ICON_SIZE, ICON_SIZE)
            else:
                # For fallback shapes, show number, name and type inside
                obj.value = f"<b>[{res_num}]</b> {resource.name}\n({display_name})"
                obj.size = (DEFAULT_WIDTH, DEFAULT_HEIGHT)
            
            x, y = positions[resource.id]
            obj.position = (x, y)
            obj.apply_style_string(style)
            
            # Add as child of group to achieve proper nesting
            if parent_group:
                parent_group.add_object(obj)
            
            objects[resource.id] = obj
        
        # Create connections/edges
        for conn in request.connections:
            if conn.source not in objects or conn.target not in objects:
                logger.warning(
                    f"Connection references unknown resource: "
                    f"{conn.source} -> {conn.target}"
                )
                continue
            
            source_obj = objects[conn.source]
            target_obj = objects[conn.target]
            
            edge = drawpyo.diagram.Edge(
                page=page,
                source=source_obj,
                target=target_obj,
            )
            
            if conn.label:
                edge.value = conn.label
            
            # Set edge styling using properties instead of style string
            edge.rounded = True
            edge.strokeColor = '#0078D4'
            edge.strokeWidth = 2
            edge.endArrow = 'blockThin'
            
            # Handle line style (dashed/dotted)
            if conn.style == 'dashed':
                edge.dashed = True
            elif conn.style == 'dotted':
                edge.dashed = True
        
        # Create legend if requested
        if request.show_legend and len(request.resources) > 0:
            diagram_bottom = _calculate_diagram_bottom(positions, group_bounds)
            legend_y = diagram_bottom + GROUP_PADDING
            _create_legend(page, request.resources, START_X, legend_y)
        
        # Write the file
        file.write()
        
        # Verify file was created
        if os.path.exists(output_path):
            opened = False
            open_msg = ""
            
            # Open in VS Code if requested
            if request.open_in_vscode:
                opened = _open_in_vscode(output_path)
                if opened:
                    open_msg = "\nOpened in VS Code."
                else:
                    open_msg = (
                        "\nCould not open in VS Code. "
                        "Ensure 'code' command is in PATH and "
                        "hediet.vscode-drawio extension is installed."
                    )
            
            return DiagramResponse(
                status='success',
                path=output_path,
                message=(
                    f"Draw.io diagram generated successfully at {output_path}{open_msg}\n"
                    f"Open with VS Code Draw.io extension (hediet.vscode-drawio) "
                    f"or draw.io application to view and edit."
                ),
                opened_in_vscode=opened,
            )
        else:
            return DiagramResponse(
                status='error',
                message='Diagram file was not created. Check logs for errors.',
            )
    
    except Exception as e:
        logger.exception("Error generating Draw.io diagram")
        return DiagramResponse(
            status='error',
            message=f"Error generating diagram: {type(e).__name__}: {str(e)}",
        )


async def generate_diagram_from_text(
    description: str,
    workspace_dir: Optional[str] = None,
    filename: Optional[str] = None,
) -> DiagramResponse:
    """
    Generate a diagram from a natural language description.
    This is a placeholder for future NLP-based generation.
    Currently returns an error indicating the feature is not implemented.
    """
    return DiagramResponse(
        status='error',
        message=(
            "Natural language diagram generation is not yet implemented. "
            "Please use generate_drawio_diagram with structured resource definitions."
        ),
    )
