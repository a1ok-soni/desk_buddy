import json

from buddy import CONVERSATION_FILE, MEMORY_FILE


def load_conversation():
    try:
        with open(CONVERSATION_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_conversation(messages):
    with open(CONVERSATION_FILE, "w") as f:
        json.dump(messages, f, indent=2)


def recall():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def remember(content: str, memory_type: str) -> str:
    """
    Store a NEW long-term memory.

    Use this tool ONLY when the user explicitly asks you to remember
    something or provides information that should be saved for future
    conversations.

    Do NOT use this tool when the user asks what you already remember.
    Use get_memories for that.

    Args:
        content: The specific fact to store.
        memory_type: The category of the memory.
    """

    memories = recall()
    memory = {"content": content, "type": memory_type}

    if memory not in memories:
        memories.append(memory)

        with open(MEMORY_FILE, "w") as f:
            json.dump(memories, f, indent=2)

        return f"Memory stored: {content}"

    return f"Memory already exists: {content}"


def forget(to_remove):
    """
    Remove an existing long-term memory that matches the given text.

    Use this tool ONLY when the user explicitly asks you to forget
    or remove something you previously remembered.

    Args:
        to_remove: Text to match against stored memory content. Any
            memory containing this text will be deleted.
    """
    memories = recall()

    for memory in memories:
        if memory["content"]:
            if to_remove in memory["content"]:
                memories.remove(memory)

                with open(MEMORY_FILE, "w") as f:
                    json.dump(memories, f, indent=2)
                return f"Memory removed: {to_remove}"

    else:
        return f"Memory not found: {to_remove}"


def get_memories():
    """
    Retrieve existing long-term memories.

    Use this tool when the user asks what you remember, what you know
    about them, or asks to see/list their stored memories.

    This tool does NOT create or modify memories.
    """
    return json.dumps(recall())
