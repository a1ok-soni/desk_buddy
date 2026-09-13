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
    Store an important piece of information in Buddy's long-term memory.

    Args:
        content: The information that should be remembered.
        memory_type: The category of the memory, such as preference, personal, or project.

    Returns:
        A confirmation that the memory was stored.
    """

    memories = recall()

    memory = {
        "content": content,
        "type": memory_type
    }

    memories.append(memory)

    with open(MEMORY_FILE, "w") as f:
        json.dump(memories, f, indent=2)

    return f"Memory stored: {content}"
