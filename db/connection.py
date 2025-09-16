import psycopg2
from psycopg2.extras import RealDictCursor
from config.config import Config

cfg = Config()

def get_connection():
    db_cfg = cfg.database

    return psycopg2.connect(
        dbname=db_cfg.get("name"),
        user=db_cfg.get("user"),
        password=db_cfg.get("password"),
        host=db_cfg.get("host"),
        port=db_cfg.get("port"),
        cursor_factory=RealDictCursor
    )
