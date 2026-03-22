# 使用 Python 3.14 作为基础镜像
FROM python:3.14-slim

# 设置工作目录
WORKDIR /app

# 安装 uv 包管理器
RUN pip install --upgrade pip && pip install uv

# 复制项目文件
COPY . .

# 使用 uv 安装依赖
RUN uv pip install -e .

# 设置环境变量
ENV SIYUAN_URL=http://localhost:6806
ENV SIYUAN_TOKEN=your-token-here

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "server.py"]
