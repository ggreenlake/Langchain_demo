import json
from db.connection import get_connection
from utils.config_loader import load_yaml 

def upload_yaml(yaml_path: str, table: str, as_json=False, ai_id: int = None):
    """
    上传 YAML 到指定表 (AIs, Scenes, Affection_levels)

    :param yaml_path: YAML 文件路径
    :param table: 目标表名 ("AIs" | "Scenes" | "Affection_levels")
    :param as_json: 是否以 JSONB 格式存储 (默认 False，存原始 YAML)
    :param ai_id: 如果是 Scenes 或 Affection_levels 必须提供
    """
    if as_json:
        data_dict = load_yaml(yaml_path)
        data = json.dumps(data_dict, ensure_ascii=False)
        column_type = "to_jsonb(%s::json)"
    else:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = f.read()
        column_type = "%s"

    conn = get_connection()
    cursor = conn.cursor()

    try:
        if table == "AIs":
            cursor.execute(
                f"""
                INSERT INTO AIs (profile)
                VALUES ({column_type})
                RETURNING ai_id;
                """,
                (data,)
            )
            new_id = cursor.fetchone()["ai_id"]
            print(f"✅ Profile 上传成功，ai_id = {new_id}")

        elif table == "Scenes":
            if ai_id is None:
                raise ValueError("❌ Scenes 表必须提供 ai_id")
            cursor.execute(
                f"""
                INSERT INTO Scenes (ai_id, scene)
                VALUES (%s, {column_type})
                RETURNING scene_id;
                """,
                (ai_id, data)
            )
            new_id = cursor.fetchone()["scene_id"]
            print(f"✅ Scene 上传成功，scene_id = {new_id}, 属于 ai_id = {ai_id}")

        elif table == "Affection_levels":
            if ai_id is None:
                raise ValueError("❌ Affection_levels 表必须提供 ai_id")
            cursor.execute(
                f"""
                INSERT INTO Affection_levels (ai_id, affection_level)
                VALUES (%s, {column_type})
                RETURNING af_id;
                """,
                (ai_id, data)
            )
            new_id = cursor.fetchone()["af_id"]
            print(f"✅ Affection level 上传成功，af_id = {new_id}, 属于 ai_id = {ai_id}")

        else:
            raise ValueError(f"❌ 不支持的表名: {table}")

        conn.commit()
        return new_id

    except Exception as e:
        conn.rollback()
        print(f"❌ 插入失败: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # 上传 profile
    ai_id = upload_yaml("D:\\my-langchain-app\\profiles\\Yuki\\profile.yaml", "AIs")

    # 上传对应的 scene
    upload_yaml("D:\\my-langchain-app\\profiles\\Yuki\\scenes\\cafe.yaml", "Scenes", ai_id=1)

    # 上传对应的 affection level
    upload_yaml("D:\\my-langchain-app\\profiles\\Yuki\\affection\\affection_rules.yaml", "Affection_levels", ai_id=1)
