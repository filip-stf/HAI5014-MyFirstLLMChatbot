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
            "content": "Give me 5 good reasons why I should exercise every day.",
        }
    ],
    model=model_name,
    stream=True,
    stream_options={'include_usage': True}
)

usage = None
for update in response:
    if update.choices and update.choices[0].delta:
        print(update.choices[0].delta.content or "", end="")
    if update.usage:
        usage = update.usage

if usage:
    print("\n")
    for k, v in usage.dict().items():
        print(f"{k} = {v}")