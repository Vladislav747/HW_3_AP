from functools import wraps
import json
import logging
from datetime import datetime
from typing import Callable, Any
from redis_utils import redis_cache

logger = logging.getLogger(__name__)


def json_serializer(obj: Any) -> str:
    """Кастомный сериализатор для datetime и других типов"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif hasattr(obj, 'dict'):  # Для моделей Pydantic
        return obj.dict()
    raise TypeError(f"Type {type(obj)} not JSON serializable")


def cache(expire: int = 60, prefix: str = "cache"):
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                if not redis_cache.redis:
                    await redis_cache.init_redis()

                cache_key = f"{prefix}:{func.__name__}:{str(kwargs)}"

                # Получаем данные из кэша
                cached_data = await redis_cache.redis.get(cache_key)
                if cached_data:
                    return json.loads(cached_data)

                # Выполняем функцию
                result = func(*args, **kwargs)

                # Сериализуем с обработкой специальных типов
                serialized = json.dumps(result, default=json_serializer)
                print('hhere')

                await redis_cache.redis.set(cache_key, serialized, ex=expire)
                return result

            except Exception as e:
                logger.error(f"Cache error: {str(e)}")
                result = func(*args, **kwargs)
                return result

        return async_wrapper

    return decorator


async def invalidate_cache(prefix: str, *keys):
    try:
        if not redis_cache.redis:
            await redis_cache.init_redis()

        pattern = f"{prefix}:*{':*'.join(keys)}*"
        keys_to_delete = await redis_cache.redis.keys(pattern)
        if keys_to_delete:
            await redis_cache.redis.delete(*keys_to_delete)
    except Exception as e:
        logger.error(f"Cache invalidation error: {str(e)}")
