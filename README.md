# MCP Client for Testing

A minimalistic MCP client for testing MCP Server

## Setup

1. Install [uv](https://docs.astral.sh/uv/).
2. Clone the repo `git clone git@github.com:piebro/mcp-client-for-testing.git`.
3. Go into the root dir `cd mcp-client-for-testing`.

## Usage

Run `client.py` and past your `config.json`.

```bash
uv run client.py \
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