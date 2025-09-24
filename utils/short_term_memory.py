import json
import redis
import time
from typing import List, Dict
from config.config import Config
from langchain.schema import AIMessage, HumanMessage

cfg = Config()

class ShortConversationMemoryManager:
    def __init__(self, history_size=5):
        """
        :param history_size: 要保留的消息条数（不是轮数）
        """
        redis_url = cfg.redis_url()
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.history_size = history_size

    def _make_key(self, user_id: int, ai_id: int) -> str:
        return f"chat:{user_id}:{ai_id}:history"

    def add_message(self, user_id: int, ai_id: int, role: str, content: str):
        """添加一条消息到 Redis"""
        key = self._make_key(user_id, ai_id)

        if hasattr(content, "content"):
            msg_content = content.content
        else:
            msg_content = str(content)
        
        entry = json.dumps({
            "role": role,
            "content": msg_content,
            "timestamp": time.time()
        })
        # 右推入（保证顺序）
        self.redis.rpush(key, entry)
        # 只保留最近 N 条
        self.redis.ltrim(key, -self.history_size, -1)

    def get_history(self, user_id: int, ai_id: int) -> List[Dict]:
        """获取最近的消息历史，按时间顺序返回"""
        key = self._make_key(user_id, ai_id)
        entries = self.redis.lrange(key, 0, -1)
        return [json.loads(e) for e in entries]

    def clear_history(self, user_id: int, ai_id: int):
        """清空历史"""
        key = self._make_key(user_id, ai_id)
        self.redis.delete(key)
