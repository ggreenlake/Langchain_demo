FROM python:3.13-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝代码
COPY . .

# 启动命令
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
