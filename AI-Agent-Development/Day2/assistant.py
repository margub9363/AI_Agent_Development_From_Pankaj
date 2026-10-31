from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))


print("=" * 40)
print("       My AI Assistant")
print("=" * 40)

messages = []
while True:
    print("-" * 80)
    user_input = input("You: ")
    # Save the user input to the messages list
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