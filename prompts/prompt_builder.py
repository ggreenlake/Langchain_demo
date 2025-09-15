import yaml
from langchain_core.prompts import ChatPromptTemplate
from psycopg2.extras import RealDictCursor
from db.connection import get_connection  # 你已有的
from typing import Any, Dict


def map_affection_to_prompt(ai_id: int, affection_level: int) -> str:
    """
    根据 AI ID 和亲密度等级，从数据库 Affection_levels 表读取 YAML，提取对应描述。
    """
    sql = """
        SELECT affection_level
        FROM Affection_levels
        WHERE ai_id = %s
        LIMIT 1;
    """
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (ai_id,))
            row = cur.fetchone()
            if not row:
                return "Default description"

            # affection_level 存的是 YAML
            levels = yaml.safe_load(row["affection_level"]) or {}
            stage_key = f"Stage{affection_level}"
            return levels.get("levels", {}).get(stage_key, "Default description")

    finally:
        conn.close()


def build_prompt(ai_id: int, scene_id: int, affection_level: int) -> ChatPromptTemplate:
    """
    构建完整的对话 Prompt 模板，从 AIs、Scenes、Affection_levels 三张表读取 YAML 拼接。
    """
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # profile
            cur.execute("SELECT profile FROM AIs WHERE ai_id = %s LIMIT 1;", (ai_id,))
            profile_row = cur.fetchone() or {}
            profile = yaml.safe_load(profile_row.get("profile", "")) or {}

            # scene
            cur.execute("SELECT scene FROM Scenes WHERE scene_id = %s AND ai_id = %s LIMIT 1;", (scene_id, ai_id))
            scene_row = cur.fetchone() or {}
            scene = yaml.safe_load(scene_row.get("scene", "")) or {}

        affection_prompt = map_affection_to_prompt(ai_id, affection_level)

        template = f"""{profile.get('base_prompt', '')}
Scene: {scene.get('scene_prompt', '')}
Affection State: {affection_prompt}
Question: {{question}}
Answer:"""

        return ChatPromptTemplate.from_template(template)

    finally:
        conn.close()
