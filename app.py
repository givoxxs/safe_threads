from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from transformers import pipeline
import uvicorn
from typing import List, Dict
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from concurrent.futures import ThreadPoolExecutor

# Create FastAPI app
app = FastAPI(
    title="Toxic Content Classification API",
    description="API for classifying toxic content using transformers model",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the classification pipeline globally
# This loads the model once when the server starts
classifier = pipeline(
    "text-classification", 
    model="textdetox/xlmr-large-toxicity-classifier",
    device=-1  # Force CPU usage since VM likely doesn't have GPU
)

# Create a thread pool executor for concurrent processing
# Reduced thread count to avoid overloading the single vCPU
executor = ThreadPoolExecutor(max_workers=4)

# Pydantic models for request and response
class TextRequest(BaseModel):
    text: str

class BatchTextRequest(BaseModel):
    texts: List[str]

class ClassificationResponse(BaseModel):
    text: str
    label: str
    score: float
    is_toxic: bool

# Function to classify text
def classify_text(text: str) -> Dict:
    result = classifier(text)[0]
    is_toxic = result["label"] == "toxic"
    return {
        "text": text,
        "label": result["label"],
        "score": result["score"],
        "is_toxic": is_toxic
    }

# API Endpoints
@app.get("/")
async def root():
    return {"message": "Toxic Content Classification API is running"}

@app.post("/classify", response_model=ClassificationResponse)
async def classify_endpoint(request: TextRequest):
    try:
        result = classify_text(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/classify-batch", response_model=List[ClassificationResponse])
async def classify_batch_endpoint(request: BatchTextRequest):
    try:
        # Process texts in parallel using the thread pool
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            executor,
            lambda: list(map(classify_text, request.texts))
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Run the API with Uvicorn
if __name__ == "__main__":
    # Reduced to single worker since VM only has 1 vCPU
    uvicorn.run("app:app", host="0.0.0.0", port=8000, workers=1)
