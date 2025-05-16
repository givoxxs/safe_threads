FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add memory optimization for transformer models
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
ENV HF_HOME=/app/model_cache

# Copy application code
COPY . .

# Create cache directory
RUN mkdir -p /app/model_cache

# Expose port
EXPOSE 8000

# Sử dụng Gunicorn với UvicornWorker cho FastAPI
# -w 1 (1 worker - vì chỉ có 1 CPU)
# -k uvicorn worker
# --threads 2 (hợp lý với máy yếu)
CMD ["gunicorn", "app:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "-w", "1", "--threads", "2", "--timeout", "90"]