from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI 

# ENVIRONMENT SETUP
load_dotenv()
client = OpenAI()

# CHOOSE EMBEDDING MODEL - MUST MATCH INGESTION MODEL
EMBEDDINGS = OpenAIEmbeddings(
    model="text-embedding-3-large")

# CONNECT TO EXISTING VECTOR DATABASE COLLECTION

VECTOR_DB_URL = "http://localhost:6333"
COLLECTION_NAME = "docs_en"

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=EMBEDDINGS,
    collection_name=COLLECTION_NAME,
    url=VECTOR_DB_URL,
)

# ACCEPT USER QUERY

user_query = input("HUMAN QUESTION: ")

# RUN A SIMILARITY SEARCH FOR USER QUERY IN VECTOR DB

search_results = vector_db.similarity_search(user_query)

context_blocks = []

for result in search_results:
    block = f"""
Page Content:
{result.page_content}
Page Number: {result.metadata.get("page")}
"""
    context_blocks.append(block)

# SYSTEM PROMPT + LLM CALL

SYSTEM_PROMPT = f"""
You are a RAG AI Assistant.
You have been given content extracted from documents.
Each section contains:
- The text content
- The page number

Answer the user's query using ONLY this provided information.

If the answer exists:
- Respond in a clear manner by refining the text content
- Mention the relevant page number from where the content was extracted
- Do not add outside information in any scenario

If the answer does not exist:
- Clearly state that the answer does not exist in your knowledge base.

{context_blocks}
"""

response = client.responses.create(
    model="gpt-5.4-mini",
    instructions=SYSTEM_PROMPT,
    input=user_query
)

print(response.output_text)