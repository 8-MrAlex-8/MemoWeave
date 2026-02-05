#!/bin/sh
# Startup script for Railway deployment
# Railway sets PORT environment variable dynamically
exec uvicorn server:app --host 0.0.0.0 --port "${PORT:-8000}"
