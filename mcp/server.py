from mcp.server.fastmcp import FastMCP
import wikipedia
import requests

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
    url = f"http://localhost:8080/delivery/{user_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "user not found"}
    return response.json()

@mcp.tool()
def get_internal_data(topic: str):
    """
    Tool to query the internal database of the company.
    It connects to the database, searches the database for a given topic
    and provides the relevant matches related to that topic.
    """
    return {
        "status": "completed",
        "data": "this is some fake data"
    }

mcp.run(transport="streamable-http")
