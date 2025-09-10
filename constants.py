import os

# 默认环境：dev / prod
ENV = os.getenv("APP_ENV", "dev")

CONFIG_PATH = f"config/{ENV}.yaml"
