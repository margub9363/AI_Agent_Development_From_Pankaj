import asyncio

from httpx2 import Request
from openai import OpenAI
from dotenv import load_dotenv
import os

from openai.types.responses import tool

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

# Build Tool Descriptions
def build_tool_descriptions(tools):
    descriptions = ""
    for tool in tools:
        descriptions +=  f"""
        Tool : {tool.name}

        Description: {tool.description}
        --------------------------------------
        """
    return descriptions

def planner(user_request, tools):
    tool_descriptions = build_tool_descriptions(tools)
    # Then create a prompt by combining user input and Tool Description and Give this prompt to Ollama
    prompt = f"""
    You are an AI Planner.
    Available Tools
    {tool_descriptions}

    Instructions

    1. Select the best tool.
    2. Reply ONLY with the tool name.
    3. Do not explain

    User Request
    {user_request}
    """

    # Give this prompt to ollama
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Ollama returns the tool name
    tool_name = response.choices[0].message.content
    return tool_name.strip()


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

    # Step3 : Planner: Take the user input (Question). Create Tool Description for each tool. Then create a prompt by combining user input and Tool Description and give this prompt to Ollama
    user_request = input("User: ")
    tool_name = planner(user_request, tools)

    print()
    print("Planner Selected:", tool_name )
    
    # Step5: Execute the selected tool.
    tool_result = await execute_tool(client,tool_name)

    # Step6: Generate a natural language response.
    final_answer = generate_response(user_request, tool_result)
    print(final_answer)

    await disconnect(client)


def generate_response(user_request, tool_result):
    prompt=f"""
    The user asked: {user_request}
    The tool returned: {tool_result}

    Respond directly to the user in a natural, conversational way.
    Use the tool result as the factual source.
    Transform raw tool output into a human-friendly answer.
    Do not simply copy raw values when a natural senteces would be better.
    Do not add information that is not needed to answer the request.
    Do not mention tools, internal processing, or reasoning.
    Keep the response concise.
    """    
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    asyncio.run(main())


    print()