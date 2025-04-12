import argparse
import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def execute_tool(config, tool_call):
    """Run the MCP client with the given configuration and tool call."""
    print(f"Config: {config}")
    print(f"Tool call: {tool_call}")

    for server_config in config:
        server_params = StdioServerParameters(
            command=server_config.get("command"),
            args=server_config.get("args", []),
            env=server_config.get("env", {}),
        )
        print(f"Server name: {server_config.get('name')}")
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                response = await session.list_tools()
                tool_names = [tool.name for tool in response.tools]
                print("Available tools: " + ", ".join(tool_names))

                if tool_call["name"] in tool_names:
                    result = await session.call_tool(tool_call["name"], tool_call["arguments"])
                    print(f"Result: {result.content[0].text}")
                    return result.content[0].text
                else:
                    print(f"Tool '{tool_call['name']}' not found in available tools")
                    return None


async def async_main():
    parser = argparse.ArgumentParser(description="MCP Client for Testing")
    parser.add_argument("--config", type=str, help="JSON configuration string")
    parser.add_argument("--tool_call", type=str, help="Tool call to execute")

    args = parser.parse_args()
    config = json.loads(args.config)
    tool_call = json.loads(args.tool_call)

    await execute_tool(config, tool_call)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
