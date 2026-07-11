import asyncio
import os
import shlex

from agents.mcp import MCPServerStdio


async def main() -> None:
    command = os.environ["GARNET_MCP_COMMAND"]
    args = shlex.split(os.environ["GARNET_MCP_ARGS"])

    async with MCPServerStdio(
        name="garnet-git-smoke",
        params={"command": command, "args": args},
        client_session_timeout_seconds=30,
    ) as server:
        tools = await server.list_tools()

    tool_names = {tool.name for tool in tools}
    expected_tools = {"git_log", "git_status"}
    missing_tools = expected_tools - tool_names
    if missing_tools:
        raise RuntimeError(f"Missing expected MCP tools: {sorted(missing_tools)}")

    print(f"TOOLS_OK {sorted(tool_names)}")


if __name__ == "__main__":
    asyncio.run(main())
