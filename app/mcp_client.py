from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


MCP_URL = "http://127.0.0.1:8001/mcp"


async def get_mcp_instruction() -> str:

    async with streamable_http_client(MCP_URL) as (
        read_stream,
        write_stream,
    ):

        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:

            await session.initialize()

            result = await session.call_tool(
                "get_system_instruction",
                arguments={},
            )

            for content in result.content:

                if hasattr(content, "text"):
                    return content.text

            return "You are a helpful AI assistant."