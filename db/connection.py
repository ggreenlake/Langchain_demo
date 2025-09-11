import psycopg2
from psycopg2.extras import RealDictCursor
import os

#修改成你自己的数据库内容

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "ai_service_db"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "guyanzhang123"), 
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", 5432),
        cursor_factory=RealDictCursor
    )
