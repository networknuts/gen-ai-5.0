from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI 
import redis
import ast 

# ENVIRONMENT SETUP
load_dotenv()
client = OpenAI()

# CONNECT TO REDIS
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# CHOOSE EMBEDDING MODEL - MUST MATCH INGESTION MODEL
EMBEDDINGS = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# CONNECT TO EXISTING VECTOR DATABASE COLLECTION
VECTOR_DB_URL = "http://localhost:6333"
COLLECTION_NAME = "docs_en"

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=EMBEDDINGS,
    collection_name=COLLECTION_NAME,
    url=VECTOR_DB_URL,
)

print("Worker started, waiting for jobs.")

while True:
    queue_name, raw_payload = redis_client.blpop("rag:requests")
    payload = ast.literal_eval(raw_payload)
    job_id = payload['job_id']
    query = payload['query']
    
    print(f"Processing Job: {job_id}")

    search_results = vector_db.similarity_search(query)

    context_blocks = []
    for result in search_results:
        block = f"""
Page Content:
{result.page_content}
Page Number: {result.metadata.get("page")}
"""
        context_blocks.append(block)

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
        input=query
    )

    answer = response.output_text
    redis_client.set(f"rag:response:{job_id}", answer, ex=21600)

    print(f"Job: {job_id} Completed")