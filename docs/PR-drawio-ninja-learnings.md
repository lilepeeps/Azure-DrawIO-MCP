# Draw.io Ninja Learnings Integration

This PR integrates key learnings from Simon Holdsworth's [drawio-ninja](https://github.com/simonholdsworth/drawio-ninja) project to improve the reliability and structure of generated Draw.io diagrams.

## Summary of Changes

### 1. Added Validation Module (`validator.py`)

A new validation module that checks Draw.io files for structural issues that could prevent files from opening correctly:

- **XML declaration check** - Ensures the file starts with `<?xml version="1.0" encoding="UTF-8"?>`
- **Root structure validation** - Verifies required `id="0"` and `id="1"` cells exist
- **Unique ID check** - Detects duplicate cell IDs
- **Parent reference validation** - Ensures all parent references point to existing cells
- **Edge source/target validation** - Verifies edge connections reference existing vertices
- **Geometry attribute check** - Warns if `as="geometry"` is missing
- **Page mode recommendation** - Suggests infinite canvas for web documentation
- **Unsafe character detection** - Warns about unescaped `&`, `<`, `>` characters
- **HTML content support** - Properly handles valid HTML tags when `html=1` is set

### 2. Added Infinite Canvas Option (`use_infinite_canvas`)

Based on drawio-ninja research, LLMs (and humans) often default to fixed page sizes which create visible boundaries that are inappropriate for web documentation.

**New option in `DiagramRequest`:**
```python
use_infinite_canvas: bool = Field(
    False, 
    description='Use infinite canvas (page=0) instead of fixed A4 size. Better for web docs.'
)
```

**When to use:**
- `use_infinite_canvas=True` - Web documentation, embedded diagrams, content that scales
- `use_infinite_canvas=False` (default) - PDF export, printing, fixed-size layouts

### 3. XML Declaration Injection

Draw.io files without an XML declaration can fail to open reliably in some clients. The generator now ensures the XML declaration is always present:

```python
def _ensure_xml_declaration(file_path: str) -> None:
    """Ensures file starts with XML declaration based on drawio-ninja research."""
```

### 4. Post-Write Validation

Generated diagrams are now automatically validated after creation, with results included in the response message:

```python
# Validate the generated diagram structure
is_valid, val_errors, val_warnings = validate_drawio_file(output_path)
```

### 5. GitHub Instructions File

Added `.github/instructions/drawio.instructions.md` with best practices for diagram specifications:
- Resource ID naming conventions
- Resource type aliases
- Group organization patterns
- Connection styles
- Common architecture patterns
- Validation guidance

## Key Learnings from drawio-ninja

1. **Structural Requirements**
   - Every Draw.io file needs `id="0"` (root) and `id="1" parent="0"` (default layer)
   - All vertices must be created before edges to prevent orphaned references
   - Every cell needs `vertex="1"` or `edge="1"` attribute

2. **Canvas Settings**
   - `page="0"` = infinite canvas (better for web)
   - `page="1"` = fixed page with visible boundaries

3. **Common Failure Modes**
   - Missing XML declaration
   - Duplicate IDs
   - Edges referencing non-existent vertices
   - Unescaped special characters in labels

## Files Changed

- `azure_drawio_mcp_server/validator.py` - New validation module
- `azure_drawio_mcp_server/models.py` - Added `use_infinite_canvas` option
- `azure_drawio_mcp_server/drawio_generator.py` - Integrated validation and XML declaration
- `azure_drawio_mcp_server/__init__.py` - Exported validation functions
- `.github/instructions/drawio.instructions.md` - Best practices documentation

## Testing

```python
# Test validation
from azure_drawio_mcp_server.validator import validate_drawio_file, format_validation_result

is_valid, errors, warnings = validate_drawio_file('my-diagram.drawio')
print(format_validation_result(errors, warnings))

# Test infinite canvas generation
request = DiagramRequest(
    title='My Diagram',
    resources=[...],
    use_infinite_canvas=True,  # New option
)
```

## Attribution

This PR incorporates research and patterns from:
- [drawio-ninja](https://github.com/simonholdsworth/drawio-ninja) by Simon Holdsworth
- Research on LLM limitations with graph-structured data (Guan et al., 2025)
