import redis
from config import REDIS_HOST, REDIS_PORT

# Create a redis client with url
client = redis.Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    db=0,
    decode_responses=True
)

def get_redis_client() -> redis.Redis:
    return client