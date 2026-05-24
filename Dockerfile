# ============================================================
# Dockerfile - 天玺尊邸酒店管理系统 (FastAPI 后端)
# 企业级多阶段构建，最小化生产镜像
# ============================================================

# ---- 构建阶段 ----
FROM python:3.12-slim AS builder

WORKDIR /build

# 安装编译依赖（仅构建时需要）
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装到临时目录
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---- 生产阶段 ----
FROM python:3.12-slim

# 安全：使用非 root 用户运行
RUN groupadd -r hotel && useradd -r -g hotel -d /app -s /bin/false hotel

WORKDIR /app

# 从构建阶段复制已安装的依赖
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# 复制应用代码
COPY . .

# 创建日志目录
RUN mkdir -p /var/log/hotel && chown -R hotel:hotel /var/log/hotel

# 暴露端口
EXPOSE 8000

# 切换到非 root 用户
USER hotel

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/', timeout=5)" || exit 1

# 启动
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
