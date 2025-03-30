from redis import asyncio as aioredis


class RedisCache:
    def __init__(self):
        self.redis = None

    async def init_redis(self):
        self.redis = aioredis.from_url(
            "redis://redis:6379",
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=5,  # таймаут подключения
            socket_keepalive=True     # поддержание соединения
        )

        await self.redis.ping()
        print("✅ Успешное подключение к Redis")

    async def close(self):
        await self.redis.close()


redis_cache = RedisCache()
