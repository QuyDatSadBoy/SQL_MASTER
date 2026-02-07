#!/bin/bash
# Script khởi động FastAPI server với auto-reload
# Server sẽ tự động reload khi code thay đổi

cd "$(dirname "$0")"

export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=1234
export POSTGRES_DB=office_db

echo "🚀 Starting FastAPI Server on port 8222..."
echo "📂 Working directory: $(pwd)"
echo "🔄 Auto-reload: ENABLED"
echo "🐍 Conda environment: sql"
echo ""

uvicorn api.main:app --host 0.0.0.0 --port 8222 --reload
