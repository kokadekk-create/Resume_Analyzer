#!/bin/bash

# Start FastAPI backend internally
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit as the public app
streamlit run frontend/app.py \
  --server.port $PORT \
  --server.address 0.0.0.0 \
  --server.headless true