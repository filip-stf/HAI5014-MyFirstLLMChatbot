from openai import OpenAI
import os

client = OpenAI(
  api_key= os.environ["GOOGLE_API_KEY"],
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

models = client.models.list()
for model in models:
  print(model.id)