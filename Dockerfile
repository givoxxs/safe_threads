FROM python:3.9-slim

WORKDIR /app

# Cài đặt các gói cần thiết
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Tạo cache directory trước
RUN mkdir -p /app/model_cache

# Nâng cấp pip
RUN pip install --upgrade pip

# Cài đặt dependencies cơ bản
COPY requirements.txt .
# Cài đặt các gói cơ bản trước
RUN pip install --no-cache-dir fastapi uvicorn gunicorn pydantic python-dotenv python-multipart

# Cài đặt các gói AI và ML sau
RUN pip install --no-cache-dir torch==2.0.1 
RUN pip install --no-cache-dir transformers==4.35.2 tokenizers==0.14.1

# Cài đặt các gói còn lại
RUN pip install --no-cache-dir -r requirements.txt

# Thiết lập biến môi trường
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
ENV HF_HOME=/app/model_cache

# Sao chép code ứng dụng
COPY . .

# Mở cổng
EXPOSE 8000

# Sử dụng Gunicorn với UvicornWorker cho FastAPI
# -w 1 (1 worker - vì chỉ có 1 CPU)
# -k uvicorn worker
# --threads 2 (hợp lý với máy yếu)
CMD ["gunicorn", "app:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "-w", "1", "--threads", "2", "--timeout", "90"]