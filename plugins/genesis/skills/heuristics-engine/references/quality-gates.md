# Quality Gates Reference

Comprehensive quality validation gates for Genesis templates.

## Gate Overview

| Gate | Weight | Focus |
|------|--------|-------|
| Structure | 25% | File organization, directory layout |
| Syntax | 25% | JSON/YAML/HCL validity, parsing |
| Completeness | 25% | Required components, variables |
| Security | 25% | Secrets, vulnerabilities, permissions |

## Gate 1: Structure Validation (25%)

### Checks
```yaml
checks:
  - name: required_directories
    weight: 5
    test: |
      for dir in templates docs; do
        [ -d "$dir" ] || echo "FAIL: Missing $dir"
      done

  - name: genesis_manifest
    weight: 5
    test: |
      [ -f "genesis.json" ] || echo "FAIL: Missing genesis.json"

  - name: no_misplaced_files
    weight: 5
    test: |
      # Templates should be in templates/
      find . -maxdepth 1 -name "*.template" | grep -q . && \
        echo "FAIL: Template files in root"

  - name: proper_naming
    weight: 5
    test: |
      # Check kebab-case for files
      find templates -type f | while read f; do
        basename "$f" | grep -qE '^[a-z0-9.-]+$' || \
          echo "WARN: Non-kebab-case filename: $f"
      done

  - name: readme_exists
    weight: 5
    test: |
      [ -f "README.md" ] || echo "WARN: Missing README.md"
```

### Scoring
```python
def score_structure(results):
    """Calculate structure gate score (0-25)."""
    total_weight = 25
    passed_weight = sum(
        check['weight'] for check in results
        if check['status'] == 'pass'
    )
    return passed_weight
```

## Gate 2: Syntax Validation (25%)

### Checks
```yaml
checks:
  - name: json_validity
    weight: 8
    test: |
      for f in $(find . -name "*.json"); do
        jq . "$f" > /dev/null 2>&1 || echo "FAIL: Invalid JSON: $f"
      done

  - name: yaml_validity
    weight: 8
    test: |
      for f in $(find . -name "*.yml" -o -name "*.yaml"); do
        python3 -c "import yaml; yaml.safe_load(open('$f'))" 2>&1 || \
          echo "FAIL: Invalid YAML: $f"
      done

  - name: template_syntax
    weight: 5
    test: |
      for f in $(find templates -name "*.template"); do
        # Check for unclosed blocks
        grep -c '{{#' "$f" | read opens
        grep -c '{{/' "$f" | read closes
        [ "$opens" -eq "$closes" ] || echo "FAIL: Unclosed block in $f"
      done

  - name: hcl_validity
    weight: 4
    test: |
      if [ -d terraform ]; then
        terraform fmt -check -recursive terraform/ || \
          echo "WARN: Terraform format issues"
      fi
```

### Parsing Verification
```python
def verify_json(file_path):
    """Verify JSON file validity."""
    try:
        with open(file_path) as f:
            json.load(f)
        return True, None
    except json.JSONDecodeError as e:
        return False, f"Line {e.lineno}: {e.msg}"

def verify_yaml(file_path):
    """Verify YAML file validity."""
    try:
        with open(file_path) as f:
            yaml.safe_load(f)
        return True, None
    except yaml.YAMLError as e:
        return False, str(e)

def verify_template(file_path):
    """Verify GTL template syntax."""
    with open(file_path) as f:
        content = f.read()

    # Check balanced blocks
    opens = re.findall(r'\{\{#(\w+)', content)
    closes = re.findall(r'\{\{/(\w+)', content)

    if opens != closes:
        return False, "Unbalanced template blocks"

    return True, None
```

## Gate 3: Completeness Validation (25%)

### Checks
```yaml
checks:
  - name: manifest_fields
    weight: 8
    test: |
      jq -e '.name' genesis.json > /dev/null || echo "FAIL: Missing name"
      jq -e '.prompts' genesis.json > /dev/null || echo "FAIL: Missing prompts"

  - name: variables_defined
    weight: 8
    test: |
      # Extract all template variables
      VARS=$(grep -hoE '\{\{\s*[a-z_]+' templates/**/*.template | \
        sed 's/{{[ ]*//' | sort -u)

      for var in $VARS; do
        jq -e ".prompts[] | select(.name == \"$var\")" genesis.json > /dev/null || \
          echo "WARN: Undefined variable: $var"
      done

  - name: conditionals_exist
    weight: 5
    test: |
      jq -r '.conditionals | keys[]' genesis.json 2>/dev/null | while read dir; do
        [ -d "templates/$dir" ] || echo "WARN: Missing conditional dir: $dir"
      done

  - name: post_generation_valid
    weight: 4
    test: |
      jq -r '.postGeneration[]?' genesis.json 2>/dev/null | while read cmd; do
        command -v $(echo "$cmd" | awk '{print $1}') > /dev/null || \
          echo "WARN: Post-gen command not found: $cmd"
      done
```

### Variable Extraction
```python
def extract_template_variables(template_dir):
    """Extract all variables used in templates."""
    variables = set()

    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.template'):
                path = os.path.join(root, file)
                with open(path) as f:
                    content = f.read()
                    # Match {{ variable_name }}
                    matches = re.findall(r'\{\{\s*([a-z_]+)', content)
                    variables.update(matches)

    return variables

def check_variables_defined(template_dir, manifest_path):
    """Check all template variables are defined in manifest."""
    used = extract_template_variables(template_dir)

    with open(manifest_path) as f:
        manifest = json.load(f)

    defined = {p['name'] for p in manifest.get('prompts', [])}
    undefined = used - defined

    return undefined
```

## Gate 4: Security Validation (25%)

### Checks
```yaml
checks:
  - name: no_hardcoded_secrets
    weight: 10
    test: |
      PATTERNS="password=|secret=|api_key=|token=|private_key"
      grep -rn "$PATTERNS" templates/ --include="*.template" | \
        grep -v '\{\{' && echo "FAIL: Hardcoded secrets found"

  - name: no_sensitive_files
    weight: 5
    test: |
      find templates -name ".env" -o -name "*.pem" -o -name "*.key" | \
        grep -v ".example" | grep -v ".template" && \
        echo "FAIL: Sensitive files in templates"

  - name: dockerfile_security
    weight: 5
    test: |
      for df in $(find templates -name "Dockerfile*"); do
        grep -q "USER root$" "$df" && echo "WARN: Running as root in $df"
        grep -q "^USER" "$df" || echo "WARN: No non-root user in $df"
      done

  - name: workflow_secrets
    weight: 5
    test: |
      for wf in $(find templates -path "*/.github/workflows/*.yml*"); do
        grep -n "password:" "$wf" | grep -v 'secrets\.' && \
          echo "FAIL: Hardcoded password in $wf"
      done
```

### Secret Pattern Detection
```python
SECRET_PATTERNS = [
    r'password\s*[=:]\s*["\'][^"\']+["\']',
    r'secret\s*[=:]\s*["\'][^"\']+["\']',
    r'api_key\s*[=:]\s*["\'][^"\']+["\']',
    r'token\s*[=:]\s*["\'][^"\']+["\']',
    r'private_key\s*[=:]\s*["\'][^"\']+["\']',
    r'[A-Za-z0-9+/]{40,}',  # Base64-like strings
    r'-----BEGIN.*PRIVATE KEY-----',
]

def scan_for_secrets(file_path):
    """Scan file for potential hardcoded secrets."""
    findings = []

    with open(file_path) as f:
        for i, line in enumerate(f, 1):
            # Skip template variables
            if '{{' in line:
                continue

            for pattern in SECRET_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append({
                        'file': file_path,
                        'line': i,
                        'pattern': pattern,
                        'content': line.strip()[:50]
                    })

    return findings
```

## Scoring Summary

```python
def calculate_total_score(gate_results):
    """Calculate total quality score."""
    scores = {
        'structure': gate_results['structure']['score'],
        'syntax': gate_results['syntax']['score'],
        'completeness': gate_results['completeness']['score'],
        'security': gate_results['security']['score']
    }

    total = sum(scores.values())

    grade = (
        'A' if total >= 90 else
        'B' if total >= 80 else
        'C' if total >= 70 else
        'D' if total >= 60 else
        'F'
    )

    return {
        'total': total,
        'grade': grade,
        'breakdown': scores,
        'passed': total >= 70
    }
```
