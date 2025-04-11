# MCP Client for Testing

A minimalistic MCP (Model Context Protocol) client for testing tool calls in MCP servers.

## Usage

Install [uv](https://docs.astral.sh/uv/) and test a tool call in an MCP server like this:

```bash
uvx mcp-client-for-testing \
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

To use it as in your code, install the package with:

```bash
uv pip install mcp-client-for-testing 
```

and use it like this:

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

## Development

### Installation from source

1. Clone the repo `git clone git@github.com:piebro/mcp-client-for-testing.git`.
2. Go into the root dir `cd mcp-client-for-testing`.
3. Install in development mode: `uv pip install -e .`

### Building with uv

If you want to build distribution packages:

```bash
uv build
```

### Releasing a New Version

To release a new version of the package to PyPI:

1. Create and push a new Git tag following semantic versioning:
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```

The GitHub Actions workflow will automatically build and publish the package to PyPI when a new tag is pushed. The version number will be derived directly from the Git tag.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
