import os
import logging
import asyncio

from mcp.server.mcpserver import MCPServer
from starlette.responses import JSONResponse
 
# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("chatbot-mcp")


# --------------------------------------------------
# MCP Server
# --------------------------------------------------

mcp = MCPServer("ChatBot MCP")


@mcp.tool()
def get_system_instruction() -> str:
    """Return the system instruction for the chatbot."""

    return (
        "You are a helpful AI assistant. "
        "Answer clearly and concisely. "
        "Only return text responses."
    )


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@mcp.custom_route("/", methods=["GET"])
async def health_check(request):
    return JSONResponse(
        {
            "status": "ok",
            "service": "ChatBot MCP",
        }
    )


@mcp.custom_route("/health", methods=["GET"])
async def health(request):
    return JSONResponse(
        {
            "status": "healthy",
            "service": "ChatBot MCP",
        }
    )


# --------------------------------------------------
# Start Server
# --------------------------------------------------

def start_server():
    port = int(os.environ.get("PORT", 8001))

    logger.info("Starting ChatBot MCP server...")
    logger.info("Host: 0.0.0.0")
    logger.info("Port: %s", port)

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,

        # Return JSON responses
        json_response=True,

        # Keep MCP sessions alive
        stateless_http=False,
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    while True:
        try:
            start_server()

            # If mcp.run() returns unexpectedly,
            # restart the server.
            logger.warning(
                "MCP server stopped unexpectedly. "
                "Restarting in 5 seconds..."
            )

        except KeyboardInterrupt:
            logger.info("Manual shutdown requested.")
            break

        except Exception:
            logger.exception(
                "MCP server crashed. "
                "Restarting in 5 seconds..."
            )

        try:
            asyncio.run(asyncio.sleep(5))
        except Exception:
            pass
