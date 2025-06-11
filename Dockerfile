# Stage 1: Build
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim
WORKDIR /app
# Copy only the installed packages to a standard location
COPY --from=builder /root/.local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /root/.local/bin /usr/local/bin
COPY . .
# Create and switch to a non-root user
RUN useradd -m appuser && chown appuser:appuser -R /app
USER appuser
ENV PATH=/usr/local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]