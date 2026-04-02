from openai import OpenAI 
from dotenv import load_dotenv
import requests
import os
import json 

# SETUP THE ENVIRONMENT AND OPENAI CLIENT
load_dotenv()
client = OpenAI()

# CREATE OUR AI TOOL
def get_weather(zipcode):
    apikey = os.getenv("OPENWEATHERMAP_API_KEY")
    countrycode = "in"
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode},{countrycode}&appid={apikey}"
    result = requests.get(url)
    response = result.json()
    return response

# TOOL SCHEMA - BLUEPRINT WHICH TELLS AI HOW THE USER DEFINED FUNC WORKS

tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get current weather data for a city by providing its zip code",
        "parameters": {
            "type": "object",
            "properties": {
                "zipcode": {
                    "type": "string",
                    "description": "the zipcode of the location you want to get the weather of",
                }
            },
            "required": ["zipcode"]
        }
    }
]

user_query = input("HUMAN QUESTION: ")

# FIRST LLM CALL
response = client.responses.create(
    model="gpt-5.4-mini",
    input=user_query,
    tools=tools
)

tool_output = []

for item in response.output:
    if item.type == "function_call":
        args = json.loads(item.arguments)

    if item.name == "get_weather":
        result = get_weather(args['zipcode'])
        print(result)