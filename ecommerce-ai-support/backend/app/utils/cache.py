from app.config import Settings
from typing import Optional, Any
import json

settings = Settings()

class RedisCache:
    """Redis caching wrapper with graceful fallback to in-memory cache"""
    
    def __init__(self):
        self._memory: dict = {}
        self._redis_client = None
        if settings.REDIS_ENABLED:
            try:
                import redis
                self._redis_client = redis.from_url(settings.REDIS_URL, socket_connect_timeout=2)
                self._redis_client.ping()
            except Exception:
                self._redis_client = None
    
    def get(self, key: str) -> Optional[Any]:
        if self._redis_client:
            try:
                value = self._redis_client.get(key)
                return json.loads(value) if value else None
            except Exception:
                pass
        return self._memory.get(key)
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        if self._redis_client:
            try:
                self._redis_client.setex(key, ttl or settings.REDIS_TTL, json.dumps(value))
                return True
            except Exception:
                pass
        self._memory[key] = value
        return True
    
    def delete(self, key: str) -> bool:
        if self._redis_client:
            try:
                self._redis_client.delete(key)
            except Exception:
                pass
        self._memory.pop(key, None)
        return True
    
    def clear(self) -> bool:
        self._memory.clear()
        if self._redis_client:
            try:
                self._redis_client.flushdb()
            except Exception:
                pass
        return True

cache = RedisCache()
