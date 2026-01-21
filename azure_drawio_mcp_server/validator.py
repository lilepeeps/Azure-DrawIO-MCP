#!/usr/bin/env python3
"""
Draw.io diagram validation module.

Based on learnings from Simon Holdsworth's drawio-ninja project:
https://github.com/simonholdsworth/drawio-ninja

Validates structural requirements that prevent Draw.io files from opening correctly.
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Optional, Tuple


def validate_drawio_file(filepath: str) -> Tuple[bool, List[str], List[str]]:
    """
    Validate a Draw.io file against structural requirements.
    
    Based on research showing LLMs struggle with graph-structured data
    and frequently produce invalid Draw.io XML.
    
    Args:
        filepath: Path to the .drawio file to validate
        
    Returns:
        Tuple of (is_valid, errors, warnings)
        - is_valid: True if no critical errors
        - errors: List of critical errors that prevent file from opening
        - warnings: List of non-critical issues that may affect rendering
    """
    errors: List[str] = []
    warnings: List[str] = []
    
    try:
        path = Path(filepath)
        if not path.exists():
            errors.append(f"File not found: {filepath}")
            return False, errors, warnings
        
        # Read entire file for raw text scanning
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.splitlines()
        
        # Check 1: XML declaration must be first line
        if not lines or not lines[0].strip().startswith('<?xml'):
            errors.append(
                "Missing XML declaration. "
                "File must start with: <?xml version=\"1.0\" encoding=\"UTF-8\"?>"
            )
        
        # Check 2: Detect literal backslash-n sequences in value attributes
        literal_backslash_n = re.compile(r'value="[^"]*\\n[^"]*"')
        if literal_backslash_n.search(content):
            errors.append(
                "Found literal '\\n' in value attribute. "
                "Use XML entity &#xa; or <br/> with html=1 for newlines."
            )
        
        # Check 3: Detect multi-line value attributes
        for i, line in enumerate(lines, 1):
            if 'value="' in line:
                value_start = line.find('value="')
                after_value = line[value_start + 7:]
                # If no closing quote on same line, it's multi-line
                if '"' not in after_value:
                    warnings.append(
                        f"Line {i}: Multi-line value attribute detected. "
                        "Keep value on single line for reliability."
                    )
        
        # Parse XML
        tree = ET.parse(path)
        root = tree.getroot()
        
        # Check 4: Root structure exists
        mxfile = root if root.tag == 'mxfile' else root.find('mxfile')
        if mxfile is None:
            errors.append("Missing <mxfile> root element")
            return False, errors, warnings
        
        diagram = mxfile.find('diagram')
        if diagram is None:
            errors.append("Missing <diagram> element")
            return False, errors, warnings
        
        model = diagram.find('mxGraphModel')
        if model is None:
            errors.append("Missing <mxGraphModel> element")
            return False, errors, warnings
        
        graph_root = model.find('root')
        if graph_root is None:
            errors.append("Missing <root> element")
            return False, errors, warnings
        
        # Check 5: Required root cells exist
        cells = {cell.get('id'): cell for cell in graph_root.findall('mxCell')}
        
        if '0' not in cells:
            errors.append("Missing root cell (id='0')")
        
        if '1' not in cells:
            errors.append("Missing default layer (id='1')")
        elif cells['1'].get('parent') != '0':
            errors.append("Default layer (id='1') must have parent='0'")
        
        # Check 6: All IDs are unique
        all_ids = [cell.get('id') for cell in graph_root.findall('mxCell')]
        if len(all_ids) != len(set(all_ids)):
            duplicates = [id for id in all_ids if all_ids.count(id) > 1]
            errors.append(f"Duplicate IDs found: {set(duplicates)}")
        
        # Check 7: All parent references are valid
        for cell in graph_root.findall('mxCell'):
            cell_id = cell.get('id')
            parent = cell.get('parent')
            
            if parent and parent not in cells:
                errors.append(
                    f"Cell '{cell_id}' references non-existent parent '{parent}'"
                )
        
        # Check 8: All edge source/target references are valid
        for cell in graph_root.findall('mxCell'):
            if cell.get('edge') == '1':
                cell_id = cell.get('id')
                source = cell.get('source')
                target = cell.get('target')
                
                if source and source not in cells:
                    errors.append(
                        f"Edge '{cell_id}' references non-existent source '{source}'"
                    )
                
                if target and target not in cells:
                    errors.append(
                        f"Edge '{cell_id}' references non-existent target '{target}'"
                    )
        
        # Check 9: All geometry elements have as="geometry"
        for cell in graph_root.findall('mxCell'):
            geometry = cell.find('mxGeometry')
            if geometry is not None and geometry.get('as') != 'geometry':
                cell_id = cell.get('id')
                warnings.append(
                    f"Cell '{cell_id}' geometry missing as='geometry' attribute"
                )
        
        # Check 10: Page setting (recommendation, not error)
        page = model.get('page')
        if page == '1':
            page_width = model.get('pageWidth')
            page_height = model.get('pageHeight')
            if page_width and page_height:
                warnings.append(
                    f"Using fixed page size ({page_width}x{page_height}). "
                    "Consider page='0' for infinite canvas (better for web docs)."
                )
        
        # Check 11: All content cells have vertex or edge attribute
        for cell in graph_root.findall('mxCell'):
            cell_id = cell.get('id')
            if cell_id not in ['0', '1']:
                if cell.get('vertex') != '1' and cell.get('edge') != '1':
                    # Check if it's a group (swimlane)
                    style = cell.get('style', '')
                    if 'swimlane' not in style and 'group' not in style:
                        warnings.append(
                            f"Cell '{cell_id}' missing vertex='1' or edge='1' attribute"
                        )
        
        # Check 12: Check for unsafe characters in labels
        unsafe_char = re.compile(r'&(?!amp;|lt;|gt;|quot;|apos;|#\d+;|#x[0-9a-fA-F]+;)')
        # Valid HTML tags that are allowed when html=1 is set
        allowed_html_tags = re.compile(
            r'<(?:br|table|tr|td|th|b|i|u|span|div|p|font|hr|ol|ul|li|sup|sub|em|strong)'
            r'(?:\s+[^>]*)?\s*/?>|</(?:table|tr|td|th|b|i|u|span|div|p|font|ol|ul|li|sup|sub|em|strong)>',
            re.IGNORECASE
        )
        for cell in graph_root.findall('mxCell'):
            cell_id = cell.get('id')
            value = cell.get('value', '')
            style = cell.get('style', '')
            
            # Check for unescaped ampersand
            if unsafe_char.search(value):
                warnings.append(
                    f"Cell '{cell_id}' value may contain unescaped '&'. "
                    "Use 'and' or '&amp;' instead."
                )
            
            # Check for < and > (allow valid HTML tags with html=1)
            has_html = 'html=1' in style
            if '<' in value:
                if has_html:
                    # Remove allowed HTML tags and check if any < remains
                    cleaned = allowed_html_tags.sub('', value)
                    if '<' in cleaned:
                        warnings.append(
                            f"Cell '{cell_id}' value contains '<' outside valid HTML tags. "
                            "May cause XML parsing issues."
                        )
                else:
                    warnings.append(
                        f"Cell '{cell_id}' value contains '<' without html=1. "
                        "Consider escaping or using 'less than'."
                    )
        
    except ET.ParseError as e:
        errors.append(f"XML parsing error: {e}")
        return False, errors, warnings
    except Exception as e:
        errors.append(f"Unexpected validation error: {e}")
        return False, errors, warnings
    
    return len(errors) == 0, errors, warnings


def validate_drawio_content(content: str) -> Tuple[bool, List[str], List[str]]:
    """
    Validate Draw.io XML content (string) against structural requirements.
    
    Same validation as validate_drawio_file but for in-memory content.
    
    Args:
        content: XML content as string
        
    Returns:
        Tuple of (is_valid, errors, warnings)
    """
    import tempfile
    
    # Write to temp file and validate
    with tempfile.NamedTemporaryFile(
        mode='w', 
        suffix='.drawio', 
        encoding='utf-8',
        delete=False,
    ) as f:
        f.write(content)
        temp_path = f.name
    
    try:
        return validate_drawio_file(temp_path)
    finally:
        Path(temp_path).unlink(missing_ok=True)


def format_validation_result(
    errors: List[str], 
    warnings: List[str],
) -> str:
    """Format validation results as a user-friendly message."""
    lines = []
    
    if errors:
        lines.append("❌ **Critical Errors (file may not open):**")
        for err in errors:
            lines.append(f"   • {err}")
    
    if warnings:
        lines.append("⚠️ **Warnings:**")
        for warn in warnings:
            lines.append(f"   • {warn}")
    
    if not errors and not warnings:
        lines.append("✅ Diagram structure is valid!")
    
    return "\n".join(lines)
