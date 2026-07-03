from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from app.inference import PolicySummarizer


app_instances = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Initializing PolicySummarizer and loading weights...")
        app_instances["summarizer"] = PolicySummarizer()
        print("PolicySummarizer loaded successfully!")
    except Exception as e:
        print(f"Failed to load model on startup: {e}")
        raise RuntimeError(f"Startup aborted due to model loading error: {e}")
        
    yield
    app_instances.clear()

app = FastAPI(
    title="Policy Simplifier API",
    lifespan=lifespan
)

class UserInput(BaseModel):
    text: str

@app.get("/")
def health_check():
    return {"status": "healthy", "model_loaded": "summarizer" in app_instances}

@app.post("/summarize")
async def summarize(request: UserInput):
    if "summarizer" not in app_instances:
        raise HTTPException(status_code=503, detail="Model is still initializing or unavailable.")
        
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    try:
        summarizer = app_instances["summarizer"]
        summary = summarizer.summarize(request.text)

        return {
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference engine error: {str(e)}")