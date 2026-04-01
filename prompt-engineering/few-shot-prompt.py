from openai import OpenAI 
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

f = open("few-shot-prompt.txt", "r")
system_prompt = f.read()
f.close()

user_input = input("HUMAN INPUT: ")

response = client.responses.create(
    model="gpt-5.4-mini",
    instructions=system_prompt,
    input=user_input
)

print(response.output_text)