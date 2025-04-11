# MCP Client for Testing

A minimalistic MCP client for testing MCP Server

## Installation

### From PyPI using uv

```bash
uv pip install mcp-client-for-testing
```

### From Source using uv

1. Install [uv](https://docs.astral.sh/uv/).
2. Clone the repo `git clone git@github.com:piebro/mcp-client-for-testing.git`.
3. Go into the root dir `cd mcp-client-for-testing`.
4. Install in development mode: `uv pip install -e .`

## Building with uv

If you want to build distribution packages:

```bash
# Build both source and wheel distributions
uv build .

# Install from the built wheel
uv pip install dist/mcp_client_for_testing-0.1.0-py3-none-any.whl
```

## Releasing a New Version

To release a new version of the package to PyPI:

1. Create and push a new Git tag following semantic versioning:
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```

The GitHub Actions workflow will automatically build and publish the package to PyPI when a new tag is pushed. The version number will be derived directly from the Git tag.

## Usage

### As a Python package

```python
import asyncio
import json
from mcp_client_for_testing.client import execute_tool

async def main():
    config = [
        {
            "name": "name of mcp server",
            "command": "uv",
            "args": [
                "--directory", 
                "path/to/root/dir/", 
                "run", 
                "server.py"
            ],
            "env": {}
        }
    ]
    tool_call = {"name": "tool-name", "arguments": {}}
    
    await execute_tool(config, tool_call)

if __name__ == "__main__":
    asyncio.run(main())
```

### As a command-line tool

After installation, you can use the provided command-line tool:

```bash
mcp-client \
    --config '
    [
        {
            "name": "name of mcp server",
            "command": "uv",
            "args": [
                "--directory", 
                "path/to/root/dir/", 
                "run", 
                "server.py"
            ],
            "env": {}
        }
    ]
    ' \
    --tool_call '{"name": "tool-name", "arguments": {}}'
```