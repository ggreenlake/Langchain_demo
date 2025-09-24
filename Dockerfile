FROM python:3.13-slim


# 安装基础依赖（构建需要 gcc、libffi 等）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip 工具链，避免找不到某些包
RUN pip install --upgrade pip setuptools wheel

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝代码
COPY . .

# 启动命令
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
