#!/bin/bash
set -e

echo "Starting FastAPI backend on port 8000..."
PYTHONUNBUFFERED=1 uvicorn backend.api:app --host 0.0.0.0 --port 8000 &

echo "Starting Streamlit frontend on port 7860..."
exec streamlit run frontend/streamlit_app.py \
    --server.port 7860 \
    --server.address 0.0.0.0 \
    --server.headless true
