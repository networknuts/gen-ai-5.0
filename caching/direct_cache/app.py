import redis
from openai import OpenAI
from dotenv import load_dotenv
import hashlib

# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# HASHING STRATEGY
def make_key(prompt: str):
    normalized = prompt.strip().lower()
    hashed = hashlib.sha256(normalized.encode()).hexdigest()
    return f"cache:{hashed}"

# LLM RESPONSE
def ask_llm(prompt):
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )
    return response.output_text

# MAIN LOGIC

def get_answer(prompt):
    key = make_key(prompt)
    cached_output = r.get(key)
    if cached_output:
        print("Found response in CACHE")
        return cached_output

    print("INVOKING LLM CALL")

    answer = ask_llm(prompt)
    # SAVE ANSWER TO CACHE FOR FUTURE
    r.set(key,answer)

    return answer

# RUN A LOOP
while True:
    query = input("\nHUMAN: ")
    if query == "exit":
        break
    print(f"AI RESPONSE: {get_answer(query)}")