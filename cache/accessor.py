import redis


REDIS_HOST = 'localhost'
REDIS_PORT = '6379'

def get_redis_connection() -> redis.Redis:
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=0
    )