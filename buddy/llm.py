import ollama

from buddy.memory import (
    get_memories,
    load_conversation,
    save_conversation,
    recall,
    remember,
    forget,
)

from buddy.personality import PERSONALITY
from buddy.voice import speak
from buddy.listen import listen


def main() -> None:
    messages = load_conversation()

    while True:
        memory_context = ""
        user_input = listen()

        if user_input.lower() in ["exit", "quit" ,"exit.", "quit."]:
            break

        memories = recall()

        if memories:
            memory_context = "\n\nStored memories:\n" + "\n".join(
                f"- {memory['content']}" for memory in memories
            )

        messages.append({"role": "user", "content": user_input})

        messages_for_model = [
            {
                "role": "system",
                "content": (
                    PERSONALITY + "Use the following stored memories when relevant. "
                    "Do not invent memories." + memory_context
                ),
            },
            *messages,
        ]

        response = ollama.chat(
            model="rocky", messages=messages_for_model, tools=[remember, forget, get_memories]
        )

        # Check if the model wants to call a tool.
        if response.message.tool_calls:

            # Convert the Message object into a plain dictionary.
            tool_message = {
                "role": "assistant",
                "content": response.message.content,
                "tool_calls": [
                    {
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments,
                        }
                    }
                    for call in response.message.tool_calls
                ],
            }

            messages_for_model.append(tool_message)

            for tool_call in response.message.tool_calls:
                if tool_call.function.name == "remember":
                    result = remember(**tool_call.function.arguments)
                    messages_for_model.append(
                        {
                            "role": "tool",
                            "content": result,
                        }
                    )

                elif tool_call.function.name == "forget":
                    result = forget(**tool_call.function.arguments)
                    messages_for_model.append(
                        {
                            "role": "tool",
                            "content": result,
                        }
                    )

                elif tool_call.function.name == "get_memories":
                    result = get_memories()
                    messages_for_model.append(
                        {
                            "role": "tool",
                            "content": result,
                        }
                    )

            # Ask Buddy for the final response after
            # the tool has executed.
            final_response = ollama.chat(model="rocky", messages=messages_for_model)
            content = final_response.message.content

        else:
            content = response.message.content

        print(f"Rocky: {content}")
        speak(content)
        messages.append({"role": "assistant", "content": content})
        save_conversation(messages)


if __name__ == "__main__":
    main()
