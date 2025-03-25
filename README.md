# Toxic Content Classification API

A FastAPI application for classifying toxic content, optimized for Azure VM with Standard B1ms (1 vCPU, 2 GiB RAM).

## Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application (Local Development)

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 1
```

### Run on Azure VM

For optimal performance on Azure VM with limited resources:

```bash
# Make the startup script executable
chmod +x azure_startup.sh

# Run the startup script
./azure_startup.sh
```

## API Endpoints

### Classify Single Text

```
POST /classify
```

Request body:
```json
{
  "text": "Your text to classify"
}
```

### Batch Classification

```
POST /classify-batch
```

Request body:
```json
{
  "texts": ["Text 1", "Text 2", "Text 3"]
}
```

## Docker Deployment

```bash
docker build -t toxic-content-classifier . 
docker run -p 8000:8000 toxic-content-classifier
```

## API Documentation

When the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Performance Considerations

### Expected Performance on Azure Standard B1ms (1 vCPU, 2 GiB RAM)

With the current optimization settings:
- Maximum concurrent users: ~15-20 users/second
- Average response time: 400-800ms for single text classification
- Batch processing: Recommended for higher throughput (5-10 texts per batch)

Performance bottlenecks:
1. **Memory constraint (2GB RAM)**: The transformer model requires ~800-1000MB of RAM
2. **CPU limitation (1 vCPU)**: Text classification is CPU-intensive
3. **Burst capabilities**: The B1ms instance can burst CPU performance for short periods

Recommendations for higher throughput:
- Use batch endpoint instead of individual requests
- Implement client-side rate limiting
- Consider implementing a queuing mechanism for production workloads
- Monitor memory usage and restart the service if it exceeds 80% RAM utilization
