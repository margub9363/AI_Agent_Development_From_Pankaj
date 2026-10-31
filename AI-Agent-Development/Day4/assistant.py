from openai import OpenAI
from dotenv import load_dotenv
import os
from tool_manager import execute_tool

load_dotenv()

client = OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))


print("=" * 40)
print("       My AI Assistant")
print("=" * 40)

roles = {
    "1": "You are a friendly school teacher. Explain every concept using simple language and real-life examples.",
    "2": "You are a senior Python developer. Explain programming concepts clearly and always include Python code examples.",
    "3": "You are an experienced travel guide. Recommend places, food, transportation and travel tips.",
    "4": "You are a motivational coach. Encourage the user and give practical advice with a positive attitude.",
    "5": "You are a professional interviewer. Ask one questions at a time and provide feedback after each answer."
}

print("\n AI: Hello! I am ready to help you. Please enter your choice of role:")
for key, value in roles.items():
    print(f"{key}. {value}")
print("\n AI: Please enter your choice of role:")
choice = input("You: ")
messages = [
    {
        "role": "system",
        "content": roles.get(choice, "Ypu are a helpful AI Assistane")
    },
]
while True:
    print("-" * 80)
    user_input = input("You: ")
    # Save the user input to the messages list

    tool_result = execute_tool(user_input)

    if tool_result:
        print("\nAI :", tool_result)
        continue

    messages.append({"role": "user", "content": user_input})

    if user_input.lower() in ["quit", "exit", "bye"]:
        print("Assistant: Goodbye!")
        break
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages
    )
    print(response.choices[0].message.content)
    # Save the assistant response to the messages list
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    print("-" * 80)