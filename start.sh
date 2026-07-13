#!/bin/bash
set -e

uvicorn backend.api:app --host 0.0.0.0 --port 8000 &
API_PID=$!

streamlit run frontend/streamlit_app.py --server.port 7860 --server.address 0.0.0.0 &
UI_PID=$!

wait -n $API_PID $UI_PID
kill $API_PID $UI_PID 2>/dev/null || true
