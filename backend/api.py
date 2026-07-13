from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from app.inference import PolicySummarizer
from app.config import *
import json
import re
import ast


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

def parse_list(sample):
    sample=sample.strip()
    sample=sample.strip("[]")
    
    if sample.strip()=="":
        return []
        
    items=[]
    for item in sample.split(","):
        item=item.strip()
        item=item.strip('"')
        item=item.strip("'")
        
        if item:
            items.append(item)
            
    return items

def parse_risk_json(raw_output: str):
    try:
        return json.loads(raw_output)
    except:
        pass
    
    try:
        return ast.literal_eval(raw_output)
    except:
        pass
    
    result={k:[] for k in VALID_KINDS}
    
    raw_output=raw_output.strip()
    raw_output=raw_output.strip("{}")
    
    pattern=r'["\']?(\w+)["\']?\s*:\s*\[(.*?)\]'
    matches=re.findall(pattern,raw_output,flags=re.DOTALL)
    
    for cat,cat_list in matches:
        cat=cat.strip().strip('"').strip("'")
        
        if cat not in result:
            continue
        
        result[cat]=parse_list(cat_list)
        
    return result
         

def merge_risks(risk_outputs):
    merged = {k: set() for k in VALID_KINDS}

    for raw_output in risk_outputs:
        parsed = parse_risk_json(raw_output)

        for category, evidence_list in parsed.items():
            if category not in merged:
                continue

            for evidence in evidence_list:
                merged[category].add(evidence)

    return {k: list(v) for k, v in merged.items()}

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
        summaries,risk_statements = summarizer.generate_output(request.text)
        
        risks=merge_risks(risk_statements)

        return {
            "summaries": summaries,
            "risk_statements":risks,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference engine error: {str(e)}")
