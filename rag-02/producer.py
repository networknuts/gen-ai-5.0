import redis
import uuid 

# SETUP THE REDIS CONNECTION

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# SEND PAYLOAD TO QUEUE

def send_query(query):
    job_id = str(uuid.uuid4())
    payload = {
        "job_id": job_id,
        "query": query
    }
    redis_client.rpush("rag:requests",str(payload))
    return job_id 

user_query = input("Human Question: ")
job = send_query(user_query)

print("Query sent to queue service successfully")
print(job)