from typing import List, Dict
from db.connection import get_connection


class LongConversationMemoryManager:

    @staticmethod
    def save_message(platform: str, user_id: int, ai_id: int, role: str, content: str):
        """存一条对话到数据库"""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO conversations (platform, user_id, ai_id, role, content)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (platform, user_id, ai_id, role, content)
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
