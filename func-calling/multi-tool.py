from openai import OpenAI 
from dotenv import load_dotenv
import requests
import os
import json
import subprocess 

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

# SECOND TOOL

def run_shell(command): 
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout 

# TOOL SCHEMA - BLUEPRINT WHICH TELLS AI HOW THE USER DEFINED FUNC WORKS

tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get current weather data for a city by providing its zipcode. will not work if city name is provided. zip code is mandatory.",
        "parameters": {
            "type": "object",
            "properties": {
                "zipcode": {
                    "type": "string",
                    "description": "the zipcode of the city you want to get the weather of, will not work if city name is provided. zip code is mandatory.",
                }
            },
            "required": ["zipcode"]
        }
    },
    {
        "type": "function",
        "name": "run_shell",
        "description": "run shell commands",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The linux shell command to execute"
                }
            },
            "required": ["command"]
        }
    }
]

user_query = input("HUMAN QUESTION: ")

# FIRST LLM CALL
response = client.responses.create(
    model="gpt-5.4",
    input=user_query,
    tools=tools
)

tool_output = []

for item in response.output:
    if item.type == "function_call":
        args = json.loads(item.arguments)

    if item.name == "get_weather":
        result = get_weather(args['zipcode'])
    elif item.name == "run_shell":
        result = run_shell(args['command'])
        print(result)
    else:
        result = "UNKNOWN TOOL EXECUTED"

    tool_output.append({
        "type": "function_call_output",
        "call_id": item.call_id,
        "output": json.dumps({"result": result})
    })

# SECOND LLM CALL

final_response = client.responses.create(
    model="gpt-5.4",
    input=tool_output,
    previous_response_id = response.id
)
print("REFINED TOOL DATA\n")
print(final_response.output_text)