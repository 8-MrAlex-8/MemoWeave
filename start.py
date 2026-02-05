#!/usr/bin/env python3
"""Startup script for Railway deployment - handles PORT environment variable"""
import os
import sys

# Get PORT from environment variable, default to 8000
port = os.environ.get("PORT", "8000")

# Build uvicorn command
cmd = f"uvicorn server:app --host 0.0.0.0 --port {port}"

# Execute uvicorn
os.execvp("uvicorn", ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", port])
