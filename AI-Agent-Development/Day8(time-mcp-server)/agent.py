import asyncio

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load Configurations
load_dotenv()

# Create AI client
client = OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))

from mcp_client import (
    connect,
    disconnect,
    discover_tools,
    execute_tool
)

async def main():
    # Step 1 : Connect to the MCP server
    client = await connect()

    tools = await discover_tools(
        client
    )
    print()
    print("Avaialble tools")

    for tool in tools:
        print(tool.name)
    
    print()

    await disconnect(client)
    

if __name__ == "__main__":
    asyncio.run(main())