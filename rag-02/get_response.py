import redis
import time 

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

job_id = input("Enter JOB ID: ")

while True:
    result = redis_client.get(f"rag:response:{job_id}")
    if result:
        print("OUTPUT\n")
        print(result)
        break
    else:
        print("Waiting for answer")
        time.sleep(2)