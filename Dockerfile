# Based on python 3.12 slim Docker Image
FROM python:3.12-slim

# 設定工作目錄
WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制当前目录的所有内容到工作目录中
COPY . .

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 运行应用
CMD ["python", "main.py"]