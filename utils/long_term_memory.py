from typing import List, Dict
from db.connection import get_connection
from langchain.schema import AIMessage, HumanMessage


class LongConversationMemoryManager:

    @staticmethod
    def save_message(platform: str, user_id: int, ai_id: int, scene_id: int, affection_level:int, role: str, message):
        """存一条对话到数据库，兼容 AIMessage / HumanMessage / str"""
    # 判断类型并获取内容
        if isinstance(message, AIMessage) or isinstance(message, HumanMessage):
            content = message.content
        else:
            content = str(message)

        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO conversations (platform, user_id, ai_id, scene_id, affection_level_id, role, content)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (platform, user_id, ai_id, scene_id, affection_level, role, content)
                )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def get_history(platform: str, user_id: int, ai_id: int, limit: int = 50) -> List[Dict]:
        """查用户历史，默认最近 50 条"""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT role, content, created_at
                    FROM conversations
                    WHERE platform = %s AND user_id = %s AND ai_id = %s
                    ORDER BY created_at DESC
                    LIMIT %s
                    """,
                    (platform, user_id, ai_id, limit)
                )

                rows = cur.fetchall()
                return rows
        finally:
            conn.close()
