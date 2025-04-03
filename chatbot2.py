import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

token = os.environ["AZURE_AI_SECRET"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

messages = [
    SystemMessage("You are a helpful assistant."),
    UserMessage("What is the capital of France?"),
    AssistantMessage("The capital of France is Paris."),
    UserMessage("What about Spain?"),
]

response = client.complete(messages=messages, model=model_name)

print(response.choices[0].message.content)