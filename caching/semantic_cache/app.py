import redis
from openai import OpenAI
from dotenv import load_dotenv
import hashlib
from qdrant_client import QdrantClient 
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid 

# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()
qdrant = QdrantClient(url="http://localhost:6333")
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

COLLECTION = "cache"

# HASHING STRATEGY
def make_key(prompt: str):
    normalized = prompt.strip().lower()
    hashed = hashlib.sha256(normalized.encode()).hexdigest()
    return f"cache:{hashed}"

# EMBEDDING MODEL
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# INIT QDRANT
def init_collection(vector_size):
    try:
        qdrant.get_collection(COLLECTION)
    except:
        qdrant.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

# LLM RESPONSE
def ask_llm(prompt):
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )
    return response.output_text

# SEMANTIC SEARCH
def search_cache(embedding):
    result = qdrant.query_points(
        collection_name=COLLECTION,
        query=embedding,
        limit=1
    )
    if len(result.points) == 0:
        return None
    point = result.points[0]
    if point.score > 0.8:
        return point.payload["answer"]
    return None

# SAVE TO QDRANT
def save_cache(prompt,embedding,answer):
    qdrant.upsert(
        collection_name=COLLECTION,
        points=[
            PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "prompt": prompt,
                "answer": answer
            }
            )
        ]
    )

# MAIN LOGIC

def get_answer(prompt):
    key = make_key(prompt)

    cached_output = r.get(key)
    if cached_output:
        print("Found response in CACHE")
        return cached_output
    
    emb = get_embedding(prompt)

    init_collection(len(emb))

    semantic = search_cache(emb)
    if semantic:
        print("Found response in QDRANT")
        r.set(key,semantic)
        return semantic

    print("INVOKING LLM CALL")

    answer = ask_llm(prompt)
    # SAVE ANSWER TO REDIS CACHE FOR FUTURE
    r.set(key,answer)
    # SAVING TO QDRANT
    save_cache(prompt,emb,answer)

    return answer

# RUN A LOOP
while True:
    query = input("\nHUMAN: ")
    if query == "exit":
        break
    print(f"AI RESPONSE: {get_answer(query)}")