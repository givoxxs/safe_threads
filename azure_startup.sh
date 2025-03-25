#!/bin/bash

# Install swapfile to help with memory constraints
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab

# Set environment variables for memory optimization
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
export TRANSFORMERS_CACHE=/app/model_cache

# Start the application with memory-optimized settings
cd /app
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 1 --limit-concurrency 20 --timeout-keep-alive 30
