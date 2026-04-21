from dotenv import load_dotenv
from langgraph.graph import StateGraph, END 
from langchain_openai import ChatOpenAI
from typing import TypedDict
import json 
from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient
import os 


# SETUP THE ENVIRONMENT AND THE MODELS 

load_dotenv()

llm = ChatOpenAI(
    model="gpt-5.4"
)

llm_developer = ChatOpenAI(
    model="gpt-4.1"
)

#llm_qa = ChatOpenAI(
#    model="gpt-5.4"
#)

MAX_RETRIES = 3 

MONGO_DB = os.getenv("MONGODB_URI")

CLIENT = MongoClient(MONGO_DB)

def llm_json(prompt):
    response = llm.invoke(
        "Return only valid code, do not return any markdown\n" + prompt
    ).content.strip()
    return json.loads(response)

# DEFINING YOUR STATE

class CodeState(TypedDict):
    user_request: str 
    code: str
    rating: int 
    retries: int #pending
    feedback: str
    status: str #failed or approved

# NODE 1: DEVELOPER AGENT

def developer_agent(state: CodeState):
    prompt = f"""
You are a NODEJS developer.
Given the user's request, write NODEJS code that can fulfill the user's request.

{state['user_request']}

If feedback is provided, improve the previous version of the code accordingly.

Previous Code:
{state['code']}

Feedback:
{state['feedback']}

Return ONLY the full NODEJS code.
"""
    result = llm_developer.invoke(prompt).content
    return {
        "code": result,
        "feedback": ""
    }

# NODE 2: QA AGENT

def qa_agent(state: CodeState):
    prompt = f"""
You are a senior strict QA engineer for NODEJS.

Evaluate the given NODEJS code for the following practices:
- correctness
- structure
- readability
- production best practices
- error handling
- use of variables
- use of modules

Return a JSON in the following format:
{{
    "rating": integer between 1-10,
    "feedback": "clear explanation of improvements to be made to the code"
}}

Code:
{state['code']}
"""
    result = llm_json(prompt)
    return {
        "rating": int(result['rating']),
        "feedback": result['feedback']
    }

# NODE: CODE APPROVED

def set_approved(state: CodeState):
    return {"status": "approved"}

# NODE: CODE DENIED

def set_failed(state: CodeState):
    return {"status": "failed"}

# NODE: INCREMENTAL RETRY

def increment_retry(state: CodeState):
    return {"retries": state["retries"]+1} # 0 + 1 = 1, 1+1=2, 2+1=3


# NODE: ROUTER

def check_rating(state: CodeState):
    if state['rating'] >= 7:
        return "approved"
    if state["retries"] >= MAX_RETRIES:
        return "failed"
    return "retry"

# BUILDING THE GRAPH

graph = StateGraph(CodeState)

graph.add_node("developer", developer_agent)
graph.add_node("qa", qa_agent)
graph.add_node("approved_node", set_approved)
graph.add_node("failed_node", set_failed)
graph.add_node("increment_retry",increment_retry)

graph.set_entry_point("developer")

graph.add_edge("developer", "qa")

graph.add_conditional_edges(
    "qa",
    check_rating,
    {
        "approved": "approved_node",
        "failed": "failed_node",
        "retry": "increment_retry"
    }
)
graph.add_edge("approved_node", END)
graph.add_edge("failed_node", END)
graph.add_edge("increment_retry","developer")


MONGODB_CHECKPOINTER = MongoDBSaver(CLIENT)

app = graph.compile(checkpointer=MONGODB_CHECKPOINTER)


# EXECUTE THE GRAPH

user_id = "1002"
session_id = "2"

thread_id = f"{user_id}_{session_id}"

existing_state = MONGODB_CHECKPOINTER.get({"configurable": {"thread_id": thread_id}})

try:
    if existing_state:
        print("Resuming from checkpoint\n")
        result = app.invoke({},config={"configurable": {"thread_id": thread_id}})
    else:
        user_input = input("Explain the NODE.JS project to be built: ")
        result = app.invoke({
            "user_request": user_input,
            "code": "",
            "rating": 0,
            "feedback": "",
            "retries": 0,
            "status": "running"
        },
        config={"configurable": {"thread_id": thread_id}})

    print("\nFINAL OUTPUT\n")
    print(f"Status: {result['status']}")
    print(f"Final Rating: {result['rating']}")
    print(f"Retries Used: {result['retries']}")
    print(f"Code:\n {result['code']}")
except Exception as e:
    print(f"Error: {e}")