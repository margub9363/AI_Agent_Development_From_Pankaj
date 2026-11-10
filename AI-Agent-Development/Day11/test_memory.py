from memory import (create_database, save_memory, search_semantic_memories)

create_database()

save_memory("My Name is Rahman.",
"Nice to meet you, Rahman")

save_memory(
    "I am learning Python.",
    "Python is useful for AI development."
)

save_memory(
    "I am learning about MCP",
    "MCP allows AI applicaiotns to use tools"
)

results =  search_semantic_memories(
    "What am I learning"
)

print("\nRelevant Memories")
print("-------------------------------")

for result in results:
    print("\nScore:", result["score"])
    print("User:", result["user_message"])
    print("Assistant:",result["assistant_message"])