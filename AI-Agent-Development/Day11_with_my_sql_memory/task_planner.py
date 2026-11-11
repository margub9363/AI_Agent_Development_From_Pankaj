import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def decompose_task(user_request):

    prompt = f"""
You are an AI task planner.

Break the user's request into smaller tasks.

Rules:

1. Create only necessary tasks.
2. Put tasks in execution order.
3. Each task should be a short action.
4. Return one task per line.
5. Do not number the tasks.
6. Do not explain anything.

CRITICAL RULE:
Return no tasks (or "NONE") if the user request belongs to any of the following categories:
    1. Greetings or casual conversation (e.g., "hi", "hello", "how are you?")
    2. Introductions or personal details (e.g., "My name is Rahman", "I live in Ranchi")
    3. Memory questions about past interactions (e.g. "What is my name?", "What did we discuss earlier?")
    4. General knowledge/Q&A questions that can be answered directly without tools (e.g., "What is machine Learninig?",
        "explain gravity")

User Request:

{user_request}
"""

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "system",
                "content": "You are an AI task planner."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content.strip()

    tasks = []

    for line in result.splitlines():

        line = line.strip()

        if line:
            tasks.append(line)

    return tasks