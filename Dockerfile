# # Stage 1: Build
# FROM python:3.9-slim AS builder
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --user --no-cache-dir -r requirements.txt

# # Stage 2: Runtime
# FROM python:3.9-slim
# WORKDIR /app
# COPY --from=builder /root/.local /root/.local
# COPY . .
# ENV PATH=/root/.local/bin:$PATH
# EXPOSE 8000
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage 1: build
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .
RUN pip install --upgrade pip && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# Stage 2: final image
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /wheels /wheels
COPY --from=builder /requirements.txt .

RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
