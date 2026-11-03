import asyncio
from mcp_client import *

async def main():
    client = await connect()
    tools = await discover_tools(
        client
    )
    print()
    print("Avaialble tools")

    for tool in tools:
        print(tool.name)

    print()
    result = await execute_tool(
        client,
        "roll_dice"
    )

    print("Dice result: ", result.content[0].text)

    await disconnect(client)

asyncio.run(main())