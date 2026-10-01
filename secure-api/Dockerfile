#Builder
FROM python:3.11-alpine AS builder

WORKDIR /build

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


#Runtime
FROM python:3.11-alpine

WORKDIR /app

COPY --from=builder /install /usr/local
COPY main.py .

RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup && \
    mkdir -p /var/log/app && \
    chown -R appuser:appgroup /var/log/app

ENV LOG_DIR=/var/log/app

VOLUME ["/var/log/app"]

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://127.0.0.1:8080/health || exit 1

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
