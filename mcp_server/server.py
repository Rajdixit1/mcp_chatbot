from mcp.server.mcpserver import MCPServer


mcp = MCPServer("ChatBot MCP")


@mcp.tool()
def get_system_instruction() -> str:
    """Return the system instruction for the chatbot."""

    return (
        "You are a helpful AI assistant. "
        "Answer clearly and concisely. "
        "Only return text responses."
    )


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8001,
        json_response=True,
        stateless_http=True,
    )