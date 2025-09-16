import os
from pathlib import Path
from utils.config_loader import load_yaml


class Config:
    def __init__(self, path: str = "./config/dev.yaml"):
        self._config = load_yaml(path)

    @property
    def database(self) -> dict:
        return self._config.get("database", {})

    @property
    def redis(self) -> dict:
        return self._config.get("redis", {})

    @property
    def model(self) -> dict:
        return self._config.get("model", {})

    @property
    def log(self) -> dict:
        return self._config.get("log", {})

    @property
    def api(self) -> dict:
        return self._config.get("api", {})

    def redis_url(self) -> str:
        """拼接 Redis 连接 URL"""
        conf = self.redis
        if conf.get("password"):
            return f"redis://:{conf['password']}@{conf['host']}:{conf['port']}/{conf['db']}"
        return f"redis://{conf['host']}:{conf['port']}/{conf['db']}"

    def db_url(self) -> str:
        """拼接 PostgreSQL 连接 URL (可用于 SQLAlchemy)"""
        conf = self.database
        return (
            f"postgresql://{conf['user']}:{conf['password']}@"
            f"{conf['host']}:{conf['port']}/{conf['dbname']}"
        )
