from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from openai import OpenAI
from dotenv import load_dotenv
import json
import os
import asyncio

# -------------------------
# ENV SETUP
# -------------------------
load_dotenv()

# Fail fast if not set
MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL")
if not MCP_SERVER_URL:
    raise ValueError("MCP_SERVER_URL is not set")

client = OpenAI()

app = FastAPI()

SYSTEM_PROMPT = """
You are an MCP Client AI Assistant with access to external tools.

Decide whether to:
1. Answer directly
2. Use a tool

Then proceed accordingly.
"""

# -------------------------
# REQUEST SCHEMA
# -------------------------
class QueryRequest(BaseModel):
    query: str


# -------------------------
# TOOL CONVERTER
# -------------------------
def convert_tool(tool):
    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description or "",
        "parameters": tool.inputSchema
    }


# -------------------------
# CORE LOGIC
# -------------------------
async def process_query(query: str):
    try:
        async with streamable_http_client(MCP_SERVER_URL) as (
            read_stream,
            write_stream,
            input_stream
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                tool_list = await session.list_tools()
                tools = tool_list.tools
                openai_tools = [convert_tool(t) for t in tools]

                response = client.responses.create(
                    model="gpt-5.4-mini",
                    instructions=SYSTEM_PROMPT,
                    input=query,
                    tools=openai_tools
                )

                # Detect tool call
                tool_call = None
                for item in response.output:
                    if item.type == "function_call":
                        tool_call = item
                        break

                # Execute tool
                if tool_call:
                    tool_name = tool_call.name
                    args = json.loads(tool_call.arguments)

                    result = await asyncio.wait_for(
                        session.call_tool(tool_name, args),
                        timeout=15
                    )

                    tool_output = []
                    for item in result.content:
                        if hasattr(item, "text"):
                            tool_output.append(item.text)
                        else:
                            tool_output.append(str(item))

                    return {
                        "type": "tool",
                        "tool_name": tool_name,
                        "output": tool_output
                    }

                # Direct LLM response
                else:
                    return {
                        "type": "llm",
                        "output": response.output_text
                    }

    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Tool call timed out")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# API ENDPOINT
# -------------------------
@app.post("/ask")
async def ask(request: QueryRequest):
    return await process_query(request.query)
