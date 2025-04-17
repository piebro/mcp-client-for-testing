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
    --client_log_level "WARNING" \
	--server_log_level "INFO" \
    --tool_call '{"name": "tool-name", "arguments": {}}'
```

To use it in code, install the package:

```bash
uv pip install mcp-client-for-testing 
```

and use it like this:

```python
import asyncio
import logging
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
    
    await execute_tool(config, tool_call, server_log_level_int=logging.DEBUG)

if __name__ == "__main__":
    asyncio.run(main())
```

## Example

Use the [echo-mcp-server-for-testing](https://github.com/piebro/echo-mcp-server-for-testing) with `uvx` to test the MCP client.

```bash
uvx mcp-client-for-testing \
    --config '
    [
        {
            "name": "echo-mcp-server-for-testing",
            "command": "uvx",
            "args": [
                "echo-mcp-server-for-testing"
            ],
            "env": {
                "SECRET_KEY": "123456789"
            }
        }
    ]
    ' \
    --client_log_level "WARNING" \
	--server_log_level "INFO" \
    --tool_call '{"name": "echo_tool", "arguments": {"message": "Hello, world!"}}'
```

## Development

### Installation from source

1. Clone the repo `git clone git@github.com:piebro/mcp-client-for-testing.git`.
2. Go into the root dir `cd mcp-client-for-testing`.
3. Install in development mode: `uv pip install -e .`

### Formatting and Linting

The code is formatted and linted with ruff:

```bash
uv run ruff format
uv run ruff check --fix
```

### Building with uv

Build the package using uv:

```bash
uv build
```

### Releasing a New Version

To release a new version of the package to PyPI, create and push a new Git tag:

1. Checkout the main branch and get the current version:
   ```bash
   git checkout main
   git pull origin main
   git describe --tags
   ```

2. Create and push a new Git tag:
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```

The GitHub Actions workflow will automatically build and publish the package to PyPI when a new tag is pushed.
The python package version number will be derived directly from the Git tag.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
