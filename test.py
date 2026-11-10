from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

try:
    response = client.models.list()
    print("OpenAI connection successful!")
    print(response)
except Exception as e:
    print("OpenAI connection failed:")
    print(type(e).__name__, e)
