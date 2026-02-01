# Remediation Patterns

Strategies for fixing common plugin validation errors.

## Structure Errors

### Misplaced Components

**Error**: Components inside `.claude-plugin/`

**Detection**:
```bash
find .claude-plugin -type d -mindepth 1
```

**Fix**:
```bash
# Move directories to root
mv .claude-plugin/commands/ ./
mv .claude-plugin/agents/ ./
mv .claude-plugin/skills/ ./
```

### Missing Manifest

**Error**: No plugin.json in `.claude-plugin/`

**Detection**:
```bash
[ ! -f .claude-plugin/plugin.json ] && echo "Missing"
```

**Fix**:
```bash
mkdir -p .claude-plugin
cat > .claude-plugin/plugin.json << 'EOF'
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Plugin description"
}
EOF
```

## Schema Errors

### Invalid JSON

**Error**: JSON syntax error

**Detection**:
```bash
jq . file.json 2>&1 | grep -i error
```

**Fix**:
```python
import json

def fix_json(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Common fixes
    content = content.replace("'", '"')  # Single to double quotes
    content = re.sub(r',\s*}', '}', content)  # Trailing commas
    content = re.sub(r',\s*]', ']', content)  # Trailing commas in arrays

    # Validate
    json.loads(content)

    with open(filepath, 'w') as f:
        f.write(content)
```

### Invalid Name

**Error**: Name not kebab-case

**Detection**:
```bash
jq -r '.name' .claude-plugin/plugin.json | grep -vE '^[a-z0-9]+(-[a-z0-9]+)*$'
```

**Fix**:
```python
def fix_name(name):
    # Convert to lowercase
    name = name.lower()
    # Replace spaces and underscores with hyphens
    name = re.sub(r'[\s_]+', '-', name)
    # Remove invalid characters
    name = re.sub(r'[^a-z0-9-]', '', name)
    # Remove consecutive hyphens
    name = re.sub(r'-+', '-', name)
    # Remove leading/trailing hyphens
    name = name.strip('-')
    return name
```

## Component Errors

### Missing Frontmatter

**Error**: Markdown file without YAML frontmatter

**Detection**:
```bash
head -1 file.md | grep -v '^---'
```

**Fix**:
```python
def add_frontmatter(filepath, component_type):
    with open(filepath, 'r') as f:
        content = f.read()

    if content.startswith('---'):
        return  # Already has frontmatter

    # Default frontmatter by type
    frontmatter = FRONTMATTER_TEMPLATES[component_type]

    with open(filepath, 'w') as f:
        f.write(f"---\n{frontmatter}---\n\n{content}")
```

### Skill Too Long

**Error**: SKILL.md > 500 lines

**Detection**:
```bash
wc -l skills/*/SKILL.md | awk '$1 > 500'
```

**Fix Strategy**:
1. Identify sections > 50 lines
2. Extract to reference files
3. Add links to references
4. Verify line count

```python
def refactor_skill(skill_path):
    with open(skill_path, 'r') as f:
        lines = f.readlines()

    if len(lines) <= 500:
        return

    # Find large sections
    sections = parse_sections(lines)
    extractable = [s for s in sections if s['lines'] > 50]

    for section in extractable:
        # Create reference file
        ref_name = f"references/{section['name'].lower().replace(' ', '-')}.md"
        extract_to_reference(section, ref_name)

        # Replace with link
        replace_with_link(skill_path, section, ref_name)
```

### Missing Description

**Error**: Agent/skill without description

**Detection**:
```bash
grep -L '^description:' agents/*.md
```

**Fix**:
```python
def add_description(filepath, component_type):
    # Read file
    with open(filepath, 'r') as f:
        content = f.read()

    # Parse frontmatter
    fm, body = parse_frontmatter(content)

    # Add description based on type and name
    name = fm.get('name', os.path.basename(filepath).replace('.md', ''))
    fm['description'] = generate_description(name, component_type)

    # Write back
    write_frontmatter(filepath, fm, body)
```

## Integration Errors

### Load Error

**Error**: Plugin fails to load with `--plugin-dir`

**Detection**:
```bash
claude --plugin-dir . 2>&1 | grep -i error
```

**Common Causes & Fixes**:

1. **Invalid manifest**
   - Fix JSON syntax
   - Add required fields

2. **Missing referenced files**
   - Create missing files
   - Fix path references

3. **Invalid component syntax**
   - Fix frontmatter YAML
   - Validate component files

### Command Not Found

**Error**: Commands not appearing in `/help`

**Detection**:
```bash
claude --plugin-dir . -p "/help" 2>&1 | grep "plugin-name"
```

**Causes**:
- Wrong commands path in plugin.json
- Missing frontmatter in command files
- Invalid command file names

**Fix**:
```bash
# Verify path
jq '.commands' .claude-plugin/plugin.json

# Check files exist
ls commands/

# Verify frontmatter
head -5 commands/*.md
```

## Automated Remediation

### Fix Pipeline
```python
def remediate(error):
    """Apply fix for specific error."""
    fix_map = {
        'structure.misplaced': fix_misplaced_components,
        'schema.invalid_json': fix_json_syntax,
        'schema.invalid_name': fix_plugin_name,
        'component.missing_fm': add_frontmatter,
        'component.too_long': refactor_to_references,
        'component.no_desc': generate_description,
    }

    fixer = fix_map.get(error['type'])
    if fixer:
        return fixer(error['path'], error['details'])
    return False
```

### Batch Remediation
```python
def fix_all_errors(errors):
    """Fix all errors in priority order."""
    # Sort by priority (structure > schema > components)
    priority = ['structure', 'schema', 'component', 'integration']
    sorted_errors = sorted(errors, key=lambda e: priority.index(e['category']))

    fixed = []
    failed = []

    for error in sorted_errors:
        if remediate(error):
            fixed.append(error)
        else:
            failed.append(error)

    return fixed, failed
```
