import json
import redis
from typing import List, Dict

class ConversationMemoryManager:
    def __init__(self, redis_url="redis://localhost:6379/0", history_size=10):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.history_size = history_size

    def _make_key(self, platform: str, user_id: str) -> str:
        return f"chat:{platform}:{user_id}:history"

    def add_message(self, platform: str, user_id: str, role: str, content: str):
        """添加一条消息到 Redis"""
        key = self._make_key(platform, user_id)
        entry = json.dumps({"role": role, "content": content})
        # 左推入
        self.redis.lpush(key, entry)
        # 只保留最近 N 条
        self.redis.ltrim(key, 0, self.history_size * 2 - 1)  # user+ai 成对

    def get_history(self, platform: str, user_id: str) -> List[Dict]:
        """获取最近的消息历史，按时间顺序返回"""
        key = self._make_key(platform, user_id)
        entries = self.redis.lrange(key, 0, self.history_size * 2 - 1)
        return [json.loads(e) for e in reversed(entries)]

    def clear_history(self, platform: str, user_id: str):
        """清空历史"""
        key = self._make_key(platform, user_id)
        self.redis.delete(key)
