# Copyright (c) 2026
"""Topology-aware layout engine for Azure architecture diagrams.

This module analyzes the connection graph to determine optimal resource
positioning that minimizes edge crossings and respects data flow direction.
Supports hub-and-spoke layouts for highly-connected resources.
"""

import math
from collections import defaultdict, deque
from typing import Dict, List, Optional, Set, Tuple

from azure_drawio_mcp_server.models import AzureResource, Connection, ResourceGroup

# Hub detection threshold - resources with this many or more connections are hubs
HUB_CONNECTIVITY_THRESHOLD = 3


def build_adjacency_graph(
    connections: List[Connection],
) -> Tuple[Dict[str, List[str]], Dict[str, List[str]], Dict[str, int], Dict[str, int]]:
    """
    Build adjacency lists and degree counts from connections.
    
    Returns:
        - outgoing: Dict mapping resource ID to list of target IDs
        - incoming: Dict mapping resource ID to list of source IDs  
        - out_degree: Dict mapping resource ID to number of outgoing connections
        - in_degree: Dict mapping resource ID to number of incoming connections
    """
    outgoing: Dict[str, List[str]] = defaultdict(list)
    incoming: Dict[str, List[str]] = defaultdict(list)
    out_degree: Dict[str, int] = defaultdict(int)
    in_degree: Dict[str, int] = defaultdict(int)
    
    for conn in connections:
        outgoing[conn.source].append(conn.target)
        incoming[conn.target].append(conn.source)
        out_degree[conn.source] += 1
        in_degree[conn.target] += 1
        # Ensure all nodes exist in degree dicts
        if conn.target not in out_degree:
            out_degree[conn.target] = 0
        if conn.source not in in_degree:
            in_degree[conn.source] = 0
    
    return dict(outgoing), dict(incoming), dict(out_degree), dict(in_degree)


def assign_layers(
    resources: List[AzureResource],
    connections: List[Connection],
) -> Dict[str, int]:
    """
    Assign resources to layers using topological ordering.
    
    Layer 0 = sources (no incoming edges)
    Higher layers = resources that depend on lower layers
    
    This creates a natural left-to-right or top-to-bottom flow.
    
    Returns:
        Dict mapping resource ID to layer number (0-indexed)
    """
    resource_ids = {r.id for r in resources}
    outgoing, incoming, out_degree, in_degree = build_adjacency_graph(connections)
    
    # Find sources (nodes with no incoming edges within our resource set)
    sources = []
    for r in resources:
        if r.id not in incoming or not incoming[r.id]:
            sources.append(r.id)
        else:
            # Check if all incoming are from outside our resource set
            incoming_in_set = [s for s in incoming[r.id] if s in resource_ids]
            if not incoming_in_set:
                sources.append(r.id)
    
    # BFS to assign layers
    layers: Dict[str, int] = {}
    queue = deque()
    
    for source in sources:
        layers[source] = 0
        queue.append(source)
    
    # Process in BFS order, assigning max(parent_layer + 1)
    while queue:
        node = queue.popleft()
        current_layer = layers[node]
        
        for target in outgoing.get(node, []):
            if target not in resource_ids:
                continue
            
            # Assign to layer after current node
            new_layer = current_layer + 1
            if target not in layers:
                layers[target] = new_layer
                queue.append(target)
            else:
                # Update to max layer if we found a longer path
                if new_layer > layers[target]:
                    layers[target] = new_layer
                    queue.append(target)
    
    # Handle any disconnected resources (no connections)
    for r in resources:
        if r.id not in layers:
            layers[r.id] = 0
    
    return layers


def calculate_connectivity_score(
    resource_id: str,
    outgoing: Dict[str, List[str]],
    incoming: Dict[str, List[str]],
) -> int:
    """
    Calculate a connectivity score for a resource.
    Higher score = more connections = should be positioned centrally.
    """
    out_count = len(outgoing.get(resource_id, []))
    in_count = len(incoming.get(resource_id, []))
    return out_count + in_count


def detect_hubs(
    resources: List[AzureResource],
    connections: List[Connection],
    threshold: int = HUB_CONNECTIVITY_THRESHOLD,
) -> Dict[str, int]:
    """
    Detect hub resources based on connectivity.
    
    A hub is a resource with connections >= threshold.
    
    Returns:
        Dict mapping resource ID to connectivity score (only for hubs)
    """
    outgoing, incoming, _, _ = build_adjacency_graph(connections)
    hubs = {}
    
    for r in resources:
        score = calculate_connectivity_score(r.id, outgoing, incoming)
        if score >= threshold:
            hubs[r.id] = score
    
    return hubs


def get_connected_resources(
    hub_id: str,
    resources: List[AzureResource],
    connections: List[Connection],
) -> Tuple[List[AzureResource], List[AzureResource]]:
    """
    Get resources connected to a hub, separated by direction.
    
    Returns:
        - incoming_resources: Resources that connect TO the hub
        - outgoing_resources: Resources that the hub connects TO
    """
    resource_map = {r.id: r for r in resources}
    outgoing, incoming, _, _ = build_adjacency_graph(connections)
    
    incoming_resources = []
    outgoing_resources = []
    
    for source_id in incoming.get(hub_id, []):
        if source_id in resource_map:
            incoming_resources.append(resource_map[source_id])
    
    for target_id in outgoing.get(hub_id, []):
        if target_id in resource_map:
            outgoing_resources.append(resource_map[target_id])
    
    return incoming_resources, outgoing_resources


def calculate_radial_positions(
    hub_x: int,
    hub_y: int,
    spoke_count: int,
    radius: int,
    start_angle: float = 0,
    arc_span: float = 2 * math.pi,
) -> List[Tuple[int, int]]:
    """
    Calculate positions for spokes arranged radially around a hub.
    
    Args:
        hub_x, hub_y: Center position of the hub
        spoke_count: Number of spokes to position
        radius: Distance from hub center to spoke centers
        start_angle: Starting angle in radians (0 = right, π/2 = down)
        arc_span: Total arc span in radians (2π = full circle)
    
    Returns:
        List of (x, y) positions for each spoke
    """
    if spoke_count == 0:
        return []
    
    if spoke_count == 1:
        # Single spoke goes to the right
        angle = start_angle
        x = hub_x + int(radius * math.cos(angle))
        y = hub_y + int(radius * math.sin(angle))
        return [(x, y)]
    
    positions = []
    angle_step = arc_span / spoke_count
    
    for i in range(spoke_count):
        angle = start_angle + (i * angle_step) + (angle_step / 2)
        x = hub_x + int(radius * math.cos(angle))
        y = hub_y + int(radius * math.sin(angle))
        positions.append((x, y))
    
    return positions


def calculate_hub_spoke_layout(
    hub: AzureResource,
    spokes: List[AzureResource],
    center_x: int,
    center_y: int,
    cell_width: int,
    cell_height: int,
    incoming_spokes: Optional[List[AzureResource]] = None,
    outgoing_spokes: Optional[List[AzureResource]] = None,
) -> Dict[str, Tuple[int, int]]:
    """
    Calculate positions for a hub-and-spoke layout.
    
    Places the hub in the center and arranges spokes in a clean grid:
    - Incoming spokes on the left column
    - Hub in the center column  
    - Outgoing spokes on the right column
    
    This creates a clean left-to-right flow visualization.
    
    Args:
        hub: The hub resource
        spokes: All spoke resources (used if incoming/outgoing not specified)
        center_x, center_y: Center position for the hub
        cell_width, cell_height: Size of each resource cell
        incoming_spokes: Resources connecting TO the hub (placed left)
        outgoing_spokes: Resources the hub connects TO (placed right)
    
    Returns:
        Dict mapping resource ID to (x, y) position
    """
    positions = {}
    
    # Hub at center column
    positions[hub.id] = (center_x, center_y)
    
    if incoming_spokes is not None and outgoing_spokes is not None:
        # Grid layout: incoming on left column, hub center, outgoing on right column
        
        # Incoming spokes in left column, vertically centered
        if incoming_spokes:
            num_incoming = len(incoming_spokes)
            total_height = num_incoming * cell_height
            start_y = center_y - total_height // 2 + cell_height // 2
            
            for i, spoke in enumerate(incoming_spokes):
                x = center_x - cell_width  # One column to the left
                y = start_y + i * cell_height
                positions[spoke.id] = (x, y)
        
        # Outgoing spokes in right column, vertically centered
        if outgoing_spokes:
            num_outgoing = len(outgoing_spokes)
            total_height = num_outgoing * cell_height
            start_y = center_y - total_height // 2 + cell_height // 2
            
            for i, spoke in enumerate(outgoing_spokes):
                x = center_x + cell_width  # One column to the right
                y = start_y + i * cell_height
                positions[spoke.id] = (x, y)
    else:
        # No directional info - arrange spokes in a row below the hub
        for i, spoke in enumerate(spokes):
            cols = min(3, len(spokes))
            col = i % cols
            row = i // cols
            x = center_x - cell_width + col * cell_width
            y = center_y + cell_height + row * cell_height
            positions[spoke.id] = (x, y)
    
    return positions


def order_within_layer(
    layer_resources: List[AzureResource],
    outgoing: Dict[str, List[str]],
    incoming: Dict[str, List[str]],
    prev_layer_order: Optional[List[str]] = None,
) -> List[AzureResource]:
    """
    Order resources within a layer to minimize edge crossings.
    
    Uses barycenter heuristic: position each node at the average
    position of its connected nodes in the previous layer.
    
    Falls back to connectivity score for initial layer.
    """
    if not layer_resources:
        return []
    
    if prev_layer_order and len(prev_layer_order) > 0:
        # Use barycenter method
        def barycenter(resource: AzureResource) -> float:
            """Calculate average position of connected nodes in previous layer."""
            connected_positions = []
            
            # Check incoming connections from previous layer
            for source in incoming.get(resource.id, []):
                if source in prev_layer_order:
                    connected_positions.append(prev_layer_order.index(source))
            
            if connected_positions:
                return sum(connected_positions) / len(connected_positions)
            
            # Fall back to connectivity score
            return calculate_connectivity_score(resource.id, outgoing, incoming) * -1
        
        return sorted(layer_resources, key=barycenter)
    else:
        # First layer: order by connectivity (most connected in middle)
        scored = [(r, calculate_connectivity_score(r.id, outgoing, incoming)) 
                  for r in layer_resources]
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Place highest connectivity in middle, alternating left/right
        result = []
        left = []
        right = []
        for i, (resource, _) in enumerate(scored):
            if i == 0:
                result.append(resource)
            elif i % 2 == 1:
                left.append(resource)
            else:
                right.append(resource)
        
        return left[::-1] + result + right


def group_resources_by_layer(
    resources: List[AzureResource],
    layers: Dict[str, int],
) -> Dict[int, List[AzureResource]]:
    """Group resources by their assigned layer."""
    by_layer: Dict[int, List[AzureResource]] = defaultdict(list)
    for r in resources:
        layer = layers.get(r.id, 0)
        by_layer[layer].append(r)
    return dict(by_layer)


def optimize_group_order(
    groups: List[ResourceGroup],
    resources: List[AzureResource],
    connections: List[Connection],
) -> List[ResourceGroup]:
    """
    Reorder groups based on the topology of their contained resources.
    
    Groups containing source resources come first, groups with sinks come last.
    """
    if not groups or not connections:
        return groups
    
    # Build resource-to-group mapping
    resource_to_group: Dict[str, str] = {}
    for r in resources:
        if r.group:
            resource_to_group[r.id] = r.group
    
    # Calculate average layer per group
    layers = assign_layers(resources, connections)
    group_avg_layer: Dict[str, float] = {}
    group_resource_count: Dict[str, int] = defaultdict(int)
    group_layer_sum: Dict[str, float] = defaultdict(float)
    
    for r in resources:
        if r.group:
            group_resource_count[r.group] += 1
            group_layer_sum[r.group] += layers.get(r.id, 0)
    
    for group in groups:
        count = group_resource_count.get(group.id, 0)
        if count > 0:
            group_avg_layer[group.id] = group_layer_sum[group.id] / count
        else:
            group_avg_layer[group.id] = 0
    
    # Sort groups by average layer
    return sorted(groups, key=lambda g: group_avg_layer.get(g.id, 0))


def calculate_topology_layout(
    resources: List[AzureResource],
    groups: List[ResourceGroup],
    connections: List[Connection],
) -> Tuple[List[ResourceGroup], Dict[str, List[AzureResource]], Dict[str, int]]:
    """
    Main entry point for topology-aware layout.
    
    Analyzes the connection graph and returns:
    - Optimally ordered groups (source groups first, sink groups last)
    - Resources within each group ordered to minimize crossings
    - Hub resources identified for hub-and-spoke layout
    
    Returns:
        - ordered_groups: Groups sorted by topological order
        - group_resources: Dict mapping group ID to ordered list of resources
        - hubs: Dict mapping hub resource ID to connectivity score
    """
    # Build graph
    outgoing, incoming, _, _ = build_adjacency_graph(connections)
    
    # Assign layers
    layers = assign_layers(resources, connections)
    
    # Detect hubs
    hubs = detect_hubs(resources, connections)
    
    # Optimize group order
    ordered_groups = optimize_group_order(groups, resources, connections)
    
    # Group resources by their group
    resources_by_group: Dict[Optional[str], List[AzureResource]] = defaultdict(list)
    for r in resources:
        resources_by_group[r.group].append(r)
    
    # Order resources within each group by their layer and connectivity
    # Hubs are placed first (they'll be centered in layout)
    group_resources: Dict[str, List[AzureResource]] = {}
    
    for group in ordered_groups:
        group_res = resources_by_group.get(group.id, [])
        if group_res:
            # Sort: hubs first, then by layer, then by connectivity
            group_res_sorted = sorted(
                group_res,
                key=lambda r: (
                    0 if r.id in hubs else 1,  # Hubs first
                    layers.get(r.id, 0),
                    -calculate_connectivity_score(r.id, outgoing, incoming)
                )
            )
            group_resources[group.id] = group_res_sorted
    
    # Handle ungrouped resources
    ungrouped = resources_by_group.get(None, [])
    if ungrouped:
        ungrouped_sorted = sorted(
            ungrouped,
            key=lambda r: (
                0 if r.id in hubs else 1,  # Hubs first
                layers.get(r.id, 0),
                -calculate_connectivity_score(r.id, outgoing, incoming)
            )
        )
        group_resources[None] = ungrouped_sorted
    
    return ordered_groups, group_resources, hubs
