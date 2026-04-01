from openai import OpenAI 
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-4o",
    input="what is the capital of USA?"
)

print(response.output_text)