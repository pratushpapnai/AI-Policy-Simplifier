import evaluate
import numpy as np
from training.config import MODEL_NAME
from transformers import AutoTokenizer

rouge=evaluate.load("rouge")
tokenizer=AutoTokenizer.from_pretrained(MODEL_NAME)

def compute_metrics(eval_pred):
    preds,labels=eval_pred
    
    decode_preds=tokenizer.batch_decode(preds,skip_special_tokens=True)
    
    labels=np.where(labels!=-100,labels,tokenizer.pad_token_id)
    decode_labels=tokenizer.batch_decode(labels,skip_special_tokens=True)
    
    scores=rouge.compute(
        predictions=decode_preds,
        references=decode_labels,
        use_stemmer=True
    )
    
    return {
        "rouge1": scores["rouge1"],
        "rouge2": scores["rouge2"],
        "rougeL": scores["rougeL"],
    }