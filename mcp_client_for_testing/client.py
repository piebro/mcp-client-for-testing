# mcp_client_simple.py
import argparse
import asyncio
import json
import logging
import sys

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

log_format = "[%(levelname)s] [%(name)s] %(message)s"
formatter = logging.Formatter(log_format)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)

client_logger = logging.getLogger("mcp_client")
client_logger.addHandler(handler)


async def debug_log_handler(params: types.LoggingMessageNotificationParams, server_logger: logging.Logger):
    if params.level == "debug":
        server_logger.debug(params.data)
    elif params.level in ["info", "notice"]:
        server_logger.info(params.data)
    elif params.level in ["warning", "alert"]:
        server_logger.warning(params.data)
    elif params.level in ["error", "critical", "emergency"]:
        server_logger.error(params.data)


async def execute_tool(config, tool_call, server_log_level_int=logging.INFO):
    """Run the MCP client, connecting to servers and executing a tool."""
    client_logger.info(f"Using Config: {config}")
    client_logger.info(f"Executing Tool Call: {tool_call}")

    tool_executed = False
    final_result = None

    for server_config in config:
        server_name = server_config.get("name")
        server_params = StdioServerParameters(
            command=server_config.get("command"),
            args=server_config.get("args", []),
            env=server_config.get("env", {}),
        )
        client_logger.info(f"Attempting to connect to Server: {server_name}")

        server_logger = logging.getLogger(server_name)
        server_logger.setLevel(server_log_level_int)
        server_logger.addHandler(handler)
        logging_callback = lambda params: debug_log_handler(params, server_logger)

        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write, logging_callback=logging_callback) as session:
                    await session.initialize()
                    client_logger.debug(f"Initialized connection with {server_name}")

                    response = await session.list_tools()
                    tool_names = [tool.name for tool in response.tools]
                    client_logger.info(f"Server '{server_name}' - Available tools: " + ", ".join(tool_names))

                    if tool_call["name"] in tool_names:
                        client_logger.info(f"Calling tool '{tool_call['name']}' on server '{server_name}'")
                        result = await session.call_tool(tool_call["name"], tool_call["arguments"])
                        client_logger.info(f"Server '{server_name}' - Result: {result.content[0].text}")
                        final_result = result.content[0].text
                        tool_executed = True
                    else:
                        client_logger.debug(f"Tool '{tool_call['name']}' not found on server '{server_name}'")

        except Exception as e:
            client_logger.error(f"Failed to connect or communicate with server '{server_name}': {e}")
        finally:
            client_logger.info(f"Disconnected from Server: {server_name}")

    if not tool_executed:
        client_logger.error(f"Tool '{tool_call['name']}' not found on any configured server.")

    return final_result


async def async_main():
    parser = argparse.ArgumentParser(description="MCP Client for Testing")
    parser.add_argument("--config", required=True, type=str, help="JSON configuration string for servers")
    parser.add_argument("--tool_call", required=True, type=str, help="JSON tool call to execute")
    parser.add_argument(
        "--client_log_level",
        default="WARNING",
        type=str,
        help="Log level for client logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    parser.add_argument(
        "--server_log_level",
        default="INFO",
        type=str,
        help="Log level for server logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    args = parser.parse_args()

    client_log_level_int = LOG_LEVELS.get(args.client_log_level.upper(), logging.INFO)
    client_logger.setLevel(client_log_level_int)
    server_log_level_int = LOG_LEVELS.get(args.server_log_level.upper(), logging.INFO)

    try:
        config = json.loads(args.config)
        tool_call = json.loads(args.tool_call)
    except json.JSONDecodeError as e:
        client_logger.critical(f"Failed to parse JSON input: {e}")
        sys.exit(1)

    results = await execute_tool(config, tool_call, server_log_level_int)
    print(results)

def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        client_logger.info("Client interrupted.")


if __name__ == "__main__":
    main()
