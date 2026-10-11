from ollama import chat

response = chat(
    model = "qwen2.5:3b-instruct",
    messages = [
        {
            "role":"user",
            "content":"Explain what an API is in two simple sentences."
        }
    ]
)

print(response.message.content)