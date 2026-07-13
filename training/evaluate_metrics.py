import evaluate
import numpy as np
from transformers import AutoTokenizer

MODEL_NAME="Qwen/Qwen2.5-1.5B-Instruct"

rouge=evaluate.load("rouge")
tokenizer=AutoTokenizer.from_pretrained(MODEL_NAME)

def compute_metrics(preds,labels):
    
    scores=rouge.compute(
        predictions=preds,
        references=labels,
        use_stemmer=True
    )
    
    return {
        "rouge1": scores["rouge1"],
        "rouge2": scores["rouge2"],
        "rougeL": scores["rougeL"],
    }