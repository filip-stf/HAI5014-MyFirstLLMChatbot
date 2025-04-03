import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

token = os.environ["AZURE_AI_SECRET"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

print("Chatbot is ready! Type 'bye' to exit.")

# Initialize the conversation history
conversation_history = [
    SystemMessage("You are a helpful assistant.")
]

while True:
    user_input = input("You: ")
    if user_input.lower() == "bye":
        print("Chatbot: Goodbye!")
        break

    # Add the user's message to the conversation history
    conversation_history.append(UserMessage(user_input))

    # Get the response from the model
    response = client.complete(
        stream=True,
        messages=conversation_history,
        model_extras={'stream_options': {'include_usage': True}},
        model=model_name,
    )

    usage = {}
    assistant_reply = ""

    # Process the response and collect the assistant's reply
    for update in response:
        if update.choices and update.choices[0].delta:
            content = update.choices[0].delta.content or ""
            print(content, end="")
            assistant_reply += content
        if update.usage:
            usage = update.usage

    # Add the assistant's reply to the conversation history
    conversation_history.append(AssistantMessage(assistant_reply))

    if usage:
        print("\n")
        for k, v in usage.items():
            print(f"{k} = {v}")

client.close()