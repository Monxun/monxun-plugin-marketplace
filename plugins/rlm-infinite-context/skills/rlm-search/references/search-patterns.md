# RLM Search Patterns Reference

## Keyword Search Patterns

### Basic Keywords
Simple space-separated terms:
```
authentication login user
```
Searches for any chunk containing these terms.

### Phrase Matching
Use quotes for exact phrases:
```
"error handling"
```

### Boolean Logic (Keyword Mode)
- All keywords matched by default
- Use `match_all: true` for AND logic
- Use `match_all: false` for OR logic

## Regex Search Patterns

### Code Patterns

#### Function Definitions
```regex
# Python functions
def\s+(\w+)\s*\(

# JavaScript functions  
function\s+(\w+)\s*\(

# Async functions
async\s+(def|function)\s+(\w+)

# Class definitions
class\s+(\w+)
```

#### Error Handling
```regex
# Try/except blocks
try:\s*\n.*?except

# Error raises
raise\s+\w+Error

# Return error patterns
return\s+.*[Ee]rror
```

#### Imports
```regex
# Python imports
^(from|import)\s+[\w.]+

# JavaScript imports
import\s+.*from\s+['"]

# Require statements
require\s*\(['"]
```

### Document Patterns

#### Headers
```regex
# Markdown headers (any level)
^#{1,6}\s+.+$

# Numbered sections
^\d+\.\d*\s+.+$

# Underlined headers (Markdown)
^.+\n[=-]+$
```

#### Lists
```regex
# Bullet points
^[\s]*[-*+]\s+

# Numbered lists
^[\s]*\d+[.)]\s+
```

#### Code Blocks
```regex
# Fenced code blocks
```[\w]*\n[\s\S]*?```

# Indented code (4 spaces)
^    .+$
```

### Data Patterns

#### JSON Structure
```regex
# Object keys
"(\w+)":\s*

# Arrays
\[[\s\S]*?\]
```

#### URLs
```regex
https?://[\w\-._~:/?#\[\]@!$&'()*+,;=%]+
```

#### Dates
```regex
# ISO format
\d{4}-\d{2}-\d{2}

# Common formats
\d{1,2}/\d{1,2}/\d{2,4}
```

## Section Search Patterns

### Document Sections
```
Chapter|Section|Part|Appendix
```

### Code Sections
```
class|def|function|module|namespace
```

### Research Papers
```
Abstract|Introduction|Methods|Results|Discussion|Conclusion
```

## Advanced Patterns

### Lookahead/Lookbehind
```regex
# Find function calls (not definitions)
(?<!def\s)(\w+)\s*\(

# Find TODO comments
(?<=TODO:?\s).+
```

### Non-Greedy Matching
```regex
# Match shortest string between quotes
".*?"

# Match function body (non-greedy)
def\s+\w+\(.*?\):.*?(?=\ndef|\Z)
```

### Named Groups
```regex
# Extract function name and args
def\s+(?P<name>\w+)\s*\((?P<args>.*?)\)
```

## Pattern Optimization

### Performance Tips

1. **Anchor patterns**: Use `^` and `$` when possible
2. **Avoid catastrophic backtracking**: Be careful with nested quantifiers
3. **Use character classes**: `[a-z]` is faster than `(a|b|c|...)`
4. **Limit scope**: More specific patterns run faster

### Common Pitfalls

1. **Greedy quantifiers**: `.*` can match too much
2. **Missing escapes**: `.` matches any character, use `\.` for literal dot
3. **Unicode issues**: Use `\w` carefully with non-ASCII text

## Pattern Testing

Before using complex patterns, test them:

```python
import re
pattern = r"your_pattern_here"
test_text = """
your test content
"""
matches = re.findall(pattern, test_text, re.MULTILINE)
print(matches)
```
