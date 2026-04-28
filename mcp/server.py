from mcp.server.fastmcp import FastMCP
import wikipedia
import requests
import uvicorn 

mcp = FastMCP("Support Server", json_response=True)

# DEFINE YOUR FIRST MCP TOOL

@mcp.tool()
def wikipedia_search(topic: str):
    """
    Get wikipedia summary of any topic by providing the relevant topic name.
    This wikipedia search tool is limited to only providing a 10 line summary of the
    given topic.
    """
    try:
        return wikipedia.summary(topic,sentences=10)
    except Exception as e:
        return str(e)

# ECOMMERCE DATA TOOL

@mcp.tool()
def get_order_data(user_id: int):
    """
    Get order and delivery information for a user based upon
    the user_id.
    """
    url = f"http://ecommerce:8000/delivery/{user_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "user not found"}
    return response.json()

mcp.run(transport="streamable-http")
