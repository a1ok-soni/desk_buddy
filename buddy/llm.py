from ollama import generate

# Streaming response
print("Streaming response:")
for chunk in generate('llama3.2', 'How do I change personality of your model?', stream=True):
    print(chunk['response'], end='', flush=True)
print()  # New line at the end