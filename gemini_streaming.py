import os
from openai import OpenAI

token = os.environ["GOOGLE_API_KEY"]
endpoint = "https://generativelanguage.googleapis.com/v1beta/openai/"
model_name = "gemini-2.0-flash"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

print("Chatbot is ready! Type 'bye' to exit.")

# Initialize the conversation history
conversation_history = [
    {
        "role": "system",
        "content": "You are a helpful assistant.",
    }
]

while True:
    # Get user input
    user_input = input("You: ")
    if user_input.lower() == "bye":
        print("Chatbot: Goodbye!")
        break

    # Add the user's message to the conversation history
    conversation_history.append({
        "role": "user",
        "content": user_input,
    })

    # Get the response from the model
    response = client.chat.completions.create(
        messages=conversation_history,
        model=model_name,
        stream=True,
        stream_options={'include_usage': True}
    )

    assistant_reply = ""
    usage = None

    # Process the response and collect the assistant's reply
    for update in response:
        if update.choices and update.choices[0].delta:
            content = update.choices[0].delta.content or ""
            print(content, end="")
            assistant_reply += content
        if update.usage:
            usage = update.usage

    print("\n")  # Add a newline after the assistant's reply

    # Add the assistant's reply to the conversation history
    conversation_history.append({
        "role": "assistant",
        "content": assistant_reply,
    })

    # Print usage details if available
    if usage:
        for k, v in usage.dict().items():
            print(f"{k} = {v}")