from openai import OpenAI 
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


user_input = input("USER INPUT: ")

response = client.responses.create(
    model="gpt-5.4-mini",
    input=[
        {
            "role": "user",
            "content": "hi, my name is aryan."
        },
        {
            "role": "assistant",
            "content": "Hi Aryan — nice to meet you! How can I help today?"
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
)

print("ASSISTANT OUTPUT:\n")
print(response.output_text)