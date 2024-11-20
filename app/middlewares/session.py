from aiohttp_session import session_middleware
from aiohttp_session.redis_storage import RedisStorage
from redis.asyncio import ConnectionPool, Redis


redis_pool = ConnectionPool.from_url("redis://localhost:6379/0", max_connections=5)

redis = Redis(connection_pool=redis_pool)

redis_storage = RedisStorage(redis)

redis_session_middleware = session_middleware(redis_storage)
