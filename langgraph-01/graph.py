from dotenv import load_dotenv
from langgraph.graph import StateGraph, END 
from langchain_openai import ChatOpenAI
from typing import TypedDict

# SETUP THE ENVIRONMENT AND THE AI MODEL

load_dotenv()

llm = ChatOpenAI(
    model="gpt-5.4-nano"
)

# DEFINING THE STATE

class SupportState(TypedDict):
    user_query: str
    intent: str
    response: str 

# DEFINE NODE 1 OR AGENT 1: INTENT CLASSIFIER

def classify_intent(state: SupportState):
    prompt = f"""
    Classify the user query into one of these three categories:
    - password_reset
    - order_tracking
    - refund

    Only return the category name

    User Query: {state['user_query']}
    """
    result = llm.invoke(prompt)

    return {"intent": result.content.strip().lower()}

# NODE 2: ORDER TRACKING NODE 

def handle_order(state: SupportState):
    return {
        "response": (
            "You can track your orders from the 'My orders' section."
            "You can also track your orders by click on 'Recent Orders' in your profile"
        )
    }

# NODE 3: PASSWORD RELATED NODE

def handle_password(state: SupportState):
    return {
        "response": (
            "To reset your password, click on 'Forgot Password' in your profile"
            "Verify password reset via your email"
        )
    }

# NODE 3: REFUND RELATED NODE

def handle_refund(state: SupportState):
    return {
        "response": (
            "We have submitted your refund request to the finance team"
        )
    }

# ROUTING FUNCTION

def route_intent(state: SupportState):
    if state['intent'] == 'password_reset':
        return 'password_node'
    elif state['intent'] == 'order_tracking':
        return 'order_node'
    elif state['intent'] == 'refund':
        return 'refund_node'
    else:
        END 

# BUILD YOUR GRAPH

graph = StateGraph(SupportState)

# ADD ALL YOUR NODES

graph.add_node("classifier", classify_intent)
graph.add_node("order_node", handle_order)
graph.add_node("password_node", handle_password)
graph.add_node("refund_node", handle_refund)

graph.set_entry_point("classifier")

graph.add_conditional_edges(
    "classifier",
    route_intent
)

graph.add_edge("password_node", END)
graph.add_edge("order_node", END)
graph.add_edge("refund_node", END)


app = graph.compile()

# RUN THE APP

user_input = input("HUMAN QUERY: ")

result = app.invoke({
    "user_query": user_input,
    "intent": "",
    "response": ""
})

print(result['response'])