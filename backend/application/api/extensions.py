
import redis
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Initialize Flask-Limiter
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379"
)