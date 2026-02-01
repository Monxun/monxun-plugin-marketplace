# RLM Troubleshooting Guide

## Common Issues

### "No context loaded" Error

**Symptom:**
```json
{"error": "No context loaded. Use rlm_load first."}
```

**Causes:**
1. Context was never loaded
2. Context was cleared
3. Server restarted (contexts not persisted in memory)

**Solutions:**
```bash
# Check status
/rlm:status

# Reload context
/rlm:load ./your-document.txt
```

### Empty Search Results

**Symptom:**
```json
{"result_count": 0, "results": []}
```

**Causes:**
1. Query too specific
2. Wrong search type
3. Content not in document

**Solutions:**

1. **Broaden query:**
```bash
# Instead of
/rlm:search "getUserAuthenticationToken"

# Try
/rlm:search "authentication token"
```

2. **Check search type:**
```bash
# Try explicit types
/rlm:search "your query" --type keyword
/rlm:search "your query" --type regex
```

3. **Verify content exists:**
```bash
# Get outline to understand structure
/rlm:outline
```

### Maximum Depth Reached

**Symptom:**
```json
{"error": "Maximum recursion depth (10) reached."}
```

**Causes:**
1. Recursive loop in queries
2. Very complex information retrieval
3. Poorly targeted searches

**Solutions:**

1. **Start fresh:**
```bash
/rlm:search "new broader query"
```

2. **Use outline for targeting:**
```bash
/rlm:outline
# Then search specific sections
/rlm:search "Chapter 5 methods"
```

3. **Increase max depth (if needed):**
Set `RLM_MAX_DEPTH` environment variable.

### Regex Errors

**Symptom:**
```json
{"error": "Regex error: ..."}
```

**Common regex mistakes:**

| Error | Cause | Fix |
|-------|-------|-----|
| `unterminated subpattern` | Missing `)` | Balance parentheses |
| `nothing to repeat` | `*` or `+` at start | Add preceding pattern |
| `bad escape` | Invalid `\x` | Use raw strings or escape |

**Testing regex:**
```python
import re
try:
    re.compile(r"your pattern")
except re.error as e:
    print(f"Error: {e}")
```

### Poor Relevance Results

**Symptom:**
Results don't match what you're looking for.

**Causes:**
1. Keywords too common
2. Chunk boundaries split relevant content
3. Wrong search strategy

**Solutions:**

1. **Add context to query:**
```bash
# Instead of
/rlm:search "error"

# Try
/rlm:search "payment processing error codes"
```

2. **Increase results:**
```bash
/rlm:search "query" --top-k 20
```

3. **Use recursive search:**
```bash
# Find general area first
/rlm:search "payment module"
# Then search deeper
/rlm:search-deep "error handling" --chunks <chunk_ids>
```

### Slow Performance

**Symptom:**
Searches take several seconds.

**Causes:**
1. Very large document
2. Complex regex patterns
3. Too many chunks searched

**Solutions:**

1. **Optimize regex:**
```bash
# Avoid
/rlm:search ".*error.*" --type regex

# Use
/rlm:search "\berror\b" --type regex
```

2. **Reduce scope:**
```bash
# Use recursive search to narrow
/rlm:search-deep "specific term" --chunks 1,2,3
```

3. **Check chunk count:**
```bash
/rlm:status
# If chunks > 10000, consider loading smaller sections
```

### Memory Issues

**Symptom:**
Server crashes or becomes unresponsive.

**Causes:**
1. Document too large
2. Too many contexts loaded
3. Memory leak

**Solutions:**

1. **Clear unused contexts:**
```bash
/rlm:clear
```

2. **Load documents incrementally:**
```bash
# Instead of loading 1GB file
# Load sections separately
/rlm:load ./section1.txt --name "section1"
```

3. **Restart server:**
```bash
# In plugin directory
pkill -f "python.*rlm_server"
```

## Server Issues

### Server Not Starting

**Check logs:**
```bash
# Server logs to stderr
python -m rlm_server 2>&1 | head -50
```

**Common causes:**
1. Missing dependencies
2. Port conflict
3. Permission issues

**Solutions:**
```bash
# Check Python environment
python --version  # Need 3.8+

# Check for conflicts
lsof -i :3000  # Or whatever port

# Check permissions
ls -la ./data/
```

### MCP Connection Issues

**Symptom:**
Claude can't connect to RLM tools.

**Check .mcp.json:**
```json
{
  "mcpServers": {
    "rlm-context": {
      "command": "python",
      "args": ["-m", "rlm_server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}/servers"
    }
  }
}
```

**Verify paths:**
```bash
# Check plugin root
echo $CLAUDE_PLUGIN_ROOT

# Check server exists
ls -la ./servers/rlm_server.py
```

## Debugging Tips

### Enable Verbose Logging

```python
# In rlm_server.py
logging.basicConfig(level=logging.DEBUG)
```

### Check Tool Calls

```bash
# View recent tool calls
/rlm:status --stats
```

### Test Manually

```python
# Test server directly
import asyncio
from rlm_server import RLMServer

server = RLMServer()
result = asyncio.run(server.load_context("test content", "test"))
print(result)
```

## Getting Help

1. Check this documentation
2. Review server logs (stderr)
3. Test with simple examples first
4. File issues with reproduction steps
