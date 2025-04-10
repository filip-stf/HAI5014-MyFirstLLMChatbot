import os
from openai import OpenAI

token = os.environ["GOOGLE_API_KEY"]
endpoint = "https://generativelanguage.googleapis.com/v1beta/openai/"
model_name = "gemini-2.0-flash"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "What is the capital of France?",
        }
    ],
    temperature=1.0,
    top_p=1.0,
    max_tokens=1000,
    model=model_name
)

print(response.choices[0].message.content)