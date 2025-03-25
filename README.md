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
