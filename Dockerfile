FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add memory optimization for transformer models
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
ENV TRANSFORMERS_CACHE=/app/model_cache

# Copy application code
COPY . .

# Create cache directory
RUN mkdir -p /app/model_cache

# Expose port
EXPOSE 8000

# Run the application with reduced workers for small VM
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--limit-concurrency", "20"]