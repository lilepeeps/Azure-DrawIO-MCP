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
from azure_drawio_mcp_server.topology_layout import (
    calculate_topology_layout,
)

logger = logging.getLogger(__name__)

# A4 paper size at 96 DPI (landscape orientation for architecture diagrams)
# A4 = 297mm x 210mm = 1123 x 794 pixels at 96 DPI
A4_WIDTH = 1123
A4_HEIGHT = 794
PAGE_MARGIN = 40  # Margin from page edges

# Usable canvas area within A4
CANVAS_WIDTH = A4_WIDTH - (PAGE_MARGIN * 2)   # ~1043px
CANVAS_HEIGHT = A4_HEIGHT - (PAGE_MARGIN * 2)  # ~714px

# Grid layout constants - sized to fit icons (40px) + labels with comfortable spacing
# Generous horizontal spacing to leave room for connection labels
ICON_CELL_WIDTH = 110   # Width per icon cell (40px icon + room for edge labels)
ICON_CELL_HEIGHT = 85   # Height per icon cell (40px icon + 45px for label)
GROUP_INTERNAL_PAD = 25 # Padding inside groups around icons
GROUP_TITLE_HEIGHT = 24 # Height for group title bar
GROUP_GAP = 30          # Gap between groups (room for inter-group connections)
START_X = PAGE_MARGIN
START_Y = PAGE_MARGIN

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
    groups: List[ResourceGroup],
    connections: Optional[List[Connection]] = None,
) -> Tuple[Dict[str, Tuple[int, int]], Dict[str, Tuple[int, int, int, int]]]:
    """
    Calculate positions for resources and bounds for groups.
    Creates a CLEAN layout constrained to A4 paper size (landscape).
    
    Philosophy: Generate a good starting point that's easy to adjust.
    Users can drag icons in Draw.io to fine-tune the layout.
    
    If connections are provided, uses topology-aware ordering to place
    source resources/groups first (left) and sink resources/groups last (right).
    
    Returns:
        - positions: Dict mapping resource ID to (x, y) position
          For ungrouped resources: absolute position on page
          For grouped resources: position RELATIVE to group origin (0,0 = top-left of group)
        - group_bounds: Dict mapping group ID to (x, y, width, height)
    """
    positions: Dict[str, Tuple[int, int]] = {}
    group_bounds: Dict[str, Tuple[int, int, int, int]] = {}
    
    # Use topology-aware ordering if connections provided
    if connections:
        ordered_groups, group_resources, _ = calculate_topology_layout(
            resources, groups, connections
        )
    else:
        ordered_groups = groups
        group_resources = {}
        for r in resources:
            if r.group not in group_resources:
                group_resources[r.group] = []
            group_resources[r.group].append(r)
    
    
    # Separate resources by group (using topology order if available)
    grouped: Dict[Optional[str], List[AzureResource]] = {}
    for resource in resources:
        group_id = resource.group
        if group_id not in grouped:
            grouped[group_id] = []
        grouped[group_id].append(resource)
    
    current_x = START_X
    current_y = START_Y
    row_max_height = 0
    
    # Position ungrouped resources first (inline, left to right)
    # Use topology-ordered ungrouped resources if available
    ungrouped_resources = group_resources.get(None, grouped.get(None, []))
    if ungrouped_resources:
        for i, resource in enumerate(ungrouped_resources):
            if resource.x is not None and resource.y is not None:
                positions[resource.id] = (resource.x, resource.y)
            else:
                # Check if we need to wrap to next row
                if current_x + ICON_CELL_WIDTH > CANVAS_WIDTH + PAGE_MARGIN:
                    current_x = START_X
                    current_y += ICON_CELL_HEIGHT
                    
                positions[resource.id] = (current_x, current_y)
                current_x += ICON_CELL_WIDTH
                row_max_height = max(row_max_height, ICON_CELL_HEIGHT)
        
        # Move to new row after ungrouped resources
        current_x = START_X
        current_y += row_max_height + GROUP_GAP
        row_max_height = 0
    
    # Position groups and their resources HORIZONTALLY (left to right)
    # Uses topology-ordered groups: sources on left, sinks on right
    # Simple grid layout within groups - easy for users to adjust
    for group in ordered_groups:
        # Get topology-ordered resources for this group
        grp_resources = group_resources.get(group.id, grouped.get(group.id, []))
        if not grp_resources:
            continue
            
        num_resources = len(grp_resources)
        
        # Simple grid layout - resources flow left to right, then wrap
        # More generous spacing for easier manual adjustment
        cols = min(3, num_resources)  # Max 3 icons per row for cleaner look
        rows = (num_resources + cols - 1) // cols
        
        content_width = cols * ICON_CELL_WIDTH
        content_height = rows * ICON_CELL_HEIGHT
        
        group_width = GROUP_INTERNAL_PAD * 2 + content_width
        group_height = GROUP_TITLE_HEIGHT + GROUP_INTERNAL_PAD * 2 + content_height
        
        # Check if group fits on current row (respect A4 width)
        if current_x + group_width > CANVAS_WIDTH + PAGE_MARGIN:
            current_x = START_X
            current_y += row_max_height + GROUP_GAP
            row_max_height = 0
        
        # Position each resource RELATIVE to the group's origin
        # Resources are topology-ordered (sources first within group)
        for i, resource in enumerate(grp_resources):
            if resource.x is not None and resource.y is not None:
                positions[resource.id] = (resource.x, resource.y)
            else:
                col = i % cols
                row = i // cols
                rel_x = GROUP_INTERNAL_PAD + col * ICON_CELL_WIDTH
                rel_y = GROUP_TITLE_HEIGHT + GROUP_INTERNAL_PAD + row * ICON_CELL_HEIGHT
                positions[resource.id] = (rel_x, rel_y)
        
        # Store group bounds
        group_bounds[group.id] = (current_x, current_y, group_width, group_height)
        
        # Track max height in this row
        row_max_height = max(row_max_height, group_height)
        
        # Move to next group position (horizontal)
        current_x += group_width + GROUP_GAP
    
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
    Create a legend table at the specified position (on separate A4 page area).
    
    The legend shows numbered resources with their name, type, and rationale.
    Sized to fit within A4 width constraints.
    """
    # Calculate column widths - fit within A4 width (~1043px usable)
    COL_NUM = 35
    COL_NAME = 180
    COL_TYPE = 160
    COL_RATIONALE = 300
    TABLE_WIDTH = min(COL_NUM + COL_NAME + COL_TYPE + COL_RATIONALE, CANVAS_WIDTH)
    ROW_HEIGHT = 24
    HEADER_HEIGHT = 30
    
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


def _determine_output_path(
    workspace_dir: Optional[str],
    filename: Optional[str],
) -> Tuple[str, str]:
    """
    Determine the output directory and filename for the diagram.
    
    Handles Docker container path translation by checking if the workspace_dir
    exists and falling back to the WORKSPACE_MOUNT environment variable if needed.
    
    Args:
        workspace_dir: Requested workspace directory (may be host path in Docker)
        filename: Requested filename (will add .drawio if missing)
    
    Returns:
        Tuple of (output_directory, filename)
    """
    # Determine filename
    if filename:
        if not filename.endswith('.drawio'):
            filename = f"{filename}.drawio"
    else:
        filename = f"azure_diagram_{uuid.uuid4().hex[:8]}.drawio"
    
    # Determine output directory with Docker container support
    output_dir = None
    
    if workspace_dir:
        # Resolve workspace path, handling Docker container path translation
        workspace_path = _resolve_workspace_path(workspace_dir)
        
        if workspace_path:
            # Check if path already includes 'diagrams' subdirectory
            if 'diagrams' in workspace_path.lower():
                output_dir = workspace_path
            else:
                output_dir = os.path.join(workspace_path, 'diagrams')
    
    # Fall back to temp directory if no valid workspace found
    if not output_dir:
        output_dir = os.path.join(tempfile.gettempdir(), 'azure-drawio-diagrams')
        logger.warning(f"No valid workspace directory found, using temp: {output_dir}")
    
    return output_dir, filename


def _resolve_workspace_path(requested_path: str) -> Optional[str]:
    """
    Resolve workspace path, handling Docker container path translation.
    
    When running in Docker, the host path won't exist in the container.
    This function detects that scenario and translates to the container mount point.
    
    Args:
        requested_path: The workspace path (may be host path or container path)
    
    Returns:
        Resolved path if valid, None otherwise
    """
    # If path exists as-is, use it
    if os.path.isdir(requested_path):
        return requested_path
    
    # Path doesn't exist - check if we're in a Docker container
    container_mount = os.environ.get('WORKSPACE_MOUNT', '/workspace')
    
    if os.path.isdir(container_mount):
        logger.info(
            f"Path {requested_path} not found in container, "
            f"using container mount: {container_mount}"
        )
        return container_mount
    
    return None


def validate_diagram_request(request: DiagramRequest) -> Dict[str, List[str]]:
    """
    Validate a diagram request and provide guidance for better results.
    
    Returns a dict with 'errors', 'warnings', and 'tips' lists.
    Errors must be fixed. Warnings are recommendations. Tips are optional improvements.
    """
    result = {
        'errors': [],
        'warnings': [],
        'tips': [],
    }
    
    # Check for empty resources
    if not request.resources:
        result['errors'].append(
            "No resources specified. Add at least one AzureResource with id, name, and resource_type."
        )
        return result
    
    # Check resource types for valid icons
    from azure_drawio_mcp_server.azure_shapes import AZURE_SHAPES, RESOURCE_TYPE_ALIASES
    
    unknown_types = []
    for res in request.resources:
        resolved = RESOURCE_TYPE_ALIASES.get(res.resource_type, res.resource_type)
        if resolved not in AZURE_SHAPES:
            unknown_types.append(f"{res.name} ({res.resource_type})")
    
    if unknown_types:
        result['warnings'].append(
            f"Unknown resource types will show as gray boxes: {', '.join(unknown_types[:5])}"
            + (f" and {len(unknown_types) - 5} more" if len(unknown_types) > 5 else "")
            + ". Use common aliases like 'SQL', 'Cosmos', 'AKS', 'Functions', 'WebApp', etc."
        )
    
    # Check for groups
    if not request.groups:
        result['tips'].append(
            "Consider adding groups to organize resources visually. "
            "Groups help structure the diagram and make it easier to understand."
        )
    else:
        # Check for resources without groups
        grouped_resources = {r.id for r in request.resources if r.group}
        ungrouped = [r.name for r in request.resources if r.id not in grouped_resources]
        if ungrouped and len(ungrouped) > len(request.resources) / 2:
            result['warnings'].append(
                f"Most resources are ungrouped. Assign resources to groups using the 'group' field."
            )
    
    # Check for connections
    if not request.connections:
        result['tips'].append(
            "No connections defined. Add connections to show data flow between resources. "
            "Connections also help with automatic layout ordering."
        )
    else:
        # Check for orphan resources (no connections)
        connected_ids = set()
        for conn in request.connections:
            connected_ids.add(conn.source)
            connected_ids.add(conn.target)
        
        orphans = [r.name for r in request.resources if r.id not in connected_ids]
        if orphans:
            result['tips'].append(
                f"Some resources have no connections: {', '.join(orphans[:3])}"
                + (f" and {len(orphans) - 3} more" if len(orphans) > 3 else "")
            )
    
    # Check for duplicate IDs
    ids = [r.id for r in request.resources]
    duplicates = [id for id in ids if ids.count(id) > 1]
    if duplicates:
        result['errors'].append(
            f"Duplicate resource IDs found: {', '.join(set(duplicates))}. Each resource must have a unique id."
        )
    
    # Provide helpful tips based on resource count
    if len(request.resources) > 15:
        result['tips'].append(
            f"Large diagram with {len(request.resources)} resources. "
            "Consider breaking into multiple diagrams or using groups effectively."
        )
    
    return result


def format_validation_message(validation: Dict[str, List[str]]) -> str:
    """Format validation results as a user-friendly message."""
    lines = []
    
    if validation['errors']:
        lines.append("❌ **Errors (must fix):**")
        for err in validation['errors']:
            lines.append(f"   • {err}")
    
    if validation['warnings']:
        lines.append("⚠️ **Warnings:**")
        for warn in validation['warnings']:
            lines.append(f"   • {warn}")
    
    if validation['tips']:
        lines.append("💡 **Tips for better diagrams:**")
        for tip in validation['tips']:
            lines.append(f"   • {tip}")
    
    return "\n".join(lines)


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
        # Validate request and provide guidance
        validation = validate_diagram_request(request)
        
        # If there are errors, return early with guidance
        if validation['errors']:
            error_msg = format_validation_message(validation)
            return DiagramResponse(
                status='error',
                message=f"Validation failed:\n{error_msg}",
            )
        
        # Log warnings and tips for user awareness
        if validation['warnings'] or validation['tips']:
            guidance = format_validation_message(validation)
            logger.info(f"Diagram generation guidance:\n{guidance}")
        
        # Determine output path and filename
        output_dir, filename = _determine_output_path(
            request.workspace_dir,
            request.filename
        )
        
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)
        
        # Create Draw.io file and page
        file = drawpyo.File()
        file.file_path = output_dir
        file.file_name = filename
        
        page = drawpyo.Page(file=file)
        page.name = request.title
        # Set page to A4 landscape orientation
        page.width = A4_WIDTH   # 1123px (297mm)
        page.height = A4_HEIGHT  # 794px (210mm)
        
        # Add instruction text at top of diagram if enabled
        instructions_height = 0
        if getattr(request, 'show_instructions', True):
            instructions_text = (
                "<i>This is your generated Azure architecture diagram. "
                "Resources are organized in groups that can be moved and resized. "
                "Drag icons to reposition them — connections will auto-route. "
                "Double-click connections to add labels. "
                "Layout is optimized for A4 landscape.</i>"
            )
            instructions_obj = drawpyo_objects.Object(page=page)
            instructions_obj.value = instructions_text
            instructions_obj.position = (PAGE_MARGIN, 10)
            instructions_obj.width = CANVAS_WIDTH
            instructions_obj.height = 30
            instructions_obj.apply_style_string(
                "text;html=1;align=left;verticalAlign=middle;whiteSpace=wrap;"
                "rounded=0;fontSize=10;fontColor=#666666;strokeColor=none;fillColor=none;"
            )
            instructions_height = 35  # Add spacing below instructions
        
        # Calculate layout for all resources and groups
        # Uses topology-aware ordering when connections are provided
        positions, group_bounds = _calculate_layout(
            request.resources, 
            request.groups,
            request.connections,  # Enable topology-aware layout
        )
        
        # Offset all positions by instructions height
        if instructions_height > 0:
            # Offset group bounds
            group_bounds = {
                gid: (x, y + instructions_height, w, h) 
                for gid, (x, y, w, h) in group_bounds.items()
            }
        
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
            
            # Apply group style - use the style specified or default to box (compact)
            color = group.color or '#E6E6E6'
            group_style = group.style or 'box'
            group_obj.apply_style_string(get_group_style(color, group_style))
            
            group_objects[group.id] = group_obj
        
        # Build resource index map for numbering (matches legend order)
        resource_index = {res.id: idx + 1 for idx, res in enumerate(request.resources)}
        
        # Import alias resolver to check if resource type has an icon
        from azure_drawio_mcp_server.azure_shapes import RESOURCE_TYPE_ALIASES
        
        # Create resource shapes - nest inside groups when applicable
        for resource in request.resources:
            display_name, category, style = get_shape_info(resource.resource_type)
            
            # Determine if this resource belongs to a group
            parent_group = None
            if resource.group and resource.group in group_objects:
                parent_group = group_objects[resource.group]
            
            # Get the resource number for labeling
            res_num = resource_index.get(resource.id, 0)
            
            # Check if this resource type uses an icon (resolve aliases first)
            resolved_type = RESOURCE_TYPE_ALIASES.get(resource.resource_type, resource.resource_type)
            has_icon = (
                resolved_type in AZURE_SHAPES 
                and AZURE_SHAPES[resolved_type][2] is not None
            )
            
            # Create the object with parent set during construction for proper nesting
            # When parent is set, positions become relative to parent's origin
            if parent_group:
                obj = drawpyo_objects.Object(
                    page=page,
                    parent=parent_group,
                )
            else:
                obj = drawpyo_objects.Object(page=page)
            
            # Show numbers if explicitly requested OR if legend is shown (for cross-reference)
            show_numbers = request.show_resource_numbers or request.show_legend
            
            if has_icon:
                # For icons, show ONLY the number and user's name - clean and simple
                if show_numbers:
                    obj.value = f"[{res_num}] {resource.name}"
                else:
                    obj.value = resource.name
                obj.width = ICON_SIZE
                obj.height = ICON_SIZE
            else:
                # For fallback shapes (gray box), show name and type so user knows what it is
                if show_numbers:
                    obj.value = f"[{res_num}] {resource.name}\n({display_name})"
                else:
                    obj.value = f"{resource.name}\n({display_name})"
                obj.width = DEFAULT_WIDTH
                obj.height = DEFAULT_HEIGHT
            
            x, y = positions[resource.id]
            
            # Use position_rel_to_parent for grouped items (coordinates are already relative)
            # Use absolute position for ungrouped items
            if parent_group:
                obj.position_rel_to_parent = (x, y)
            else:
                obj.position = (x, y)
            
            obj.apply_style_string(style)
            
            objects[resource.id] = obj
        
        # Build absolute position map for edge routing
        # For grouped resources, add group origin to get absolute position
        absolute_positions: Dict[str, Tuple[int, int]] = {}
        for resource in request.resources:
            rel_x, rel_y = positions[resource.id]
            if resource.group and resource.group in group_bounds:
                gx, gy, gw, gh = group_bounds[resource.group]
                absolute_positions[resource.id] = (gx + rel_x, gy + rel_y)
            else:
                absolute_positions[resource.id] = (rel_x, rel_y)
        
        # Pre-analyze connections for edge spreading
        # Track connections per resource per direction (right/left/top/bottom)
        # Key: (resource_id, direction) -> list of connection indices
        outgoing_by_direction: Dict[Tuple[str, str], List[int]] = {}
        incoming_by_direction: Dict[Tuple[str, str], List[int]] = {}
        
        # First pass: classify each connection by direction
        connection_directions: List[Tuple[str, str]] = []  # (exit_dir, entry_dir) per connection
        for i, conn in enumerate(request.connections):
            if conn.source not in absolute_positions or conn.target not in absolute_positions:
                connection_directions.append(('right', 'left'))  # default
                continue
            
            src_x, src_y = absolute_positions[conn.source]
            tgt_x, tgt_y = absolute_positions[conn.target]
            dx = tgt_x - src_x
            dy = tgt_y - src_y
            
            # Determine direction based on relative positions
            if abs(dx) > abs(dy):
                if dx > 0:
                    exit_dir, entry_dir = 'right', 'left'
                else:
                    exit_dir, entry_dir = 'left', 'right'
            else:
                if dy > 0:
                    exit_dir, entry_dir = 'bottom', 'top'
                else:
                    exit_dir, entry_dir = 'top', 'bottom'
            
            connection_directions.append((exit_dir, entry_dir))
            
            # Track this connection for its source (outgoing) and target (incoming)
            src_key = (conn.source, exit_dir)
            tgt_key = (conn.target, entry_dir)
            
            if src_key not in outgoing_by_direction:
                outgoing_by_direction[src_key] = []
            outgoing_by_direction[src_key].append(i)
            
            if tgt_key not in incoming_by_direction:
                incoming_by_direction[tgt_key] = []
            incoming_by_direction[tgt_key].append(i)
        
        def _get_spread_position(index: int, total: int) -> float:
            """
            Calculate spread position for edge connections.
            Distributes connection points evenly along the edge.
            Returns value between 0.2 and 0.8 to stay within icon bounds.
            """
            if total == 1:
                return 0.5
            # Spread between 0.2 and 0.8 to stay within icon area
            min_pos, max_pos = 0.2, 0.8
            step = (max_pos - min_pos) / (total - 1) if total > 1 else 0
            return min_pos + (index * step)
        
        # Create connections/edges with spreading
        for i, conn in enumerate(request.connections):
            if conn.source not in objects or conn.target not in objects:
                logger.warning(
                    f"Connection references unknown resource: "
                    f"{conn.source} -> {conn.target}"
                )
                continue
            
            source_obj = objects[conn.source]
            target_obj = objects[conn.target]
            
            # Use orthogonal edges with edge-to-edge connections
            edge = drawpyo.diagram.Edge(
                page=page,
                source=source_obj,
                target=target_obj,
            )
            
            if conn.label:
                edge.value = conn.label
            
            # Get direction for this connection
            exit_dir, entry_dir = connection_directions[i]
            
            # Calculate spread positions
            src_key = (conn.source, exit_dir)
            tgt_key = (conn.target, entry_dir)
            
            # Find this connection's index within its group
            out_list = outgoing_by_direction.get(src_key, [i])
            in_list = incoming_by_direction.get(tgt_key, [i])
            out_idx = out_list.index(i) if i in out_list else 0
            in_idx = in_list.index(i) if i in in_list else 0
            
            exit_spread = _get_spread_position(out_idx, len(out_list))
            entry_spread = _get_spread_position(in_idx, len(in_list))
            
            # Apply connection points based on direction with spreading
            if exit_dir == 'right':
                edge.exitX = 1
                edge.exitY = exit_spread
            elif exit_dir == 'left':
                edge.exitX = 0
                edge.exitY = exit_spread
            elif exit_dir == 'bottom':
                edge.exitX = exit_spread
                edge.exitY = 1
            else:  # top
                edge.exitX = exit_spread
                edge.exitY = 0
            
            if entry_dir == 'left':
                edge.entryX = 0
                edge.entryY = entry_spread
            elif entry_dir == 'right':
                edge.entryX = 1
                edge.entryY = entry_spread
            elif entry_dir == 'top':
                edge.entryX = entry_spread
                edge.entryY = 0
            else:  # bottom
                edge.entryX = entry_spread
                edge.entryY = 1
            
            # Set edge properties - thin, light lines for cleaner look
            edge.endArrow = 'blockThin'
            edge.strokeColor = '#999999'  # Light gray for less visual noise
            edge.strokeWidth = 1
            edge.rounded = 1  # Enable rounded corners for cleaner routing
            
            # Apply line pattern for dashed/dotted styles
            if conn.style == 'dashed':
                edge.pattern = 'dashed'
            elif conn.style == 'dotted':
                edge.pattern = 'dotted'
        
        # Create legend if requested - placed on "second A4 page" below main diagram
        if request.show_legend and len(request.resources) > 0:
            # Place legend on a new "page" - offset by A4_HEIGHT + gap
            legend_y = A4_HEIGHT + PAGE_MARGIN  # Start of second A4 page
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
            
            # Build success message with any guidance
            guidance_msg = ""
            if validation['warnings'] or validation['tips']:
                guidance_msg = "\n\n" + format_validation_message(validation)
            
            return DiagramResponse(
                status='success',
                path=output_path,
                message=(
                    f"Draw.io diagram generated successfully at {output_path}{open_msg}\n"
                    f"Open with VS Code Draw.io extension (hediet.vscode-drawio) "
                    f"or draw.io application to view and edit."
                    f"{guidance_msg}"
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
