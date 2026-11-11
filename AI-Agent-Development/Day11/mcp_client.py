from fastmcp.client.transports.stdio import NodeStdioTransport, PythonStdioTransport


from fastmcp.client.transports.stdio import NodeStdioTransport, PythonStdioTransport


from fastmcp.client.transports.sse import SSETransport


from fastmcp.client.transports.http import StreamableHttpTransport


from fastmcp import Client
from pathlib import Path

async def connect():

    """
    Connect to the MCP Server.
    """

    # client = Client[PythonStdioTransport | NodeStdioTransport | SSETransport | StreamableHttpTransport]("server.py")
    # client = Client("server.py")
    client = Client(Path(__file__).resolve().parent / "server.py")

    await client.__aenter__()

    print("Connected to MCP Server.")

    return client


async def disconnect(client):

    """
    Close the MCP connection.
    """

    await client.__aexit__(
        None,
        None,
        None
    )


async def discover_tools(client):

    """
    Retrieve all tools from the server.
    """

    tools = await client.list_tools()

    return tools


async def execute_tool(
    client,
    tool_name,
    arguments=None
):

    """
    Execute a tool.
    """

    if arguments is None:

        arguments = {}

    result = await client.call_tool(

        tool_name,

        arguments

    )

    return result

