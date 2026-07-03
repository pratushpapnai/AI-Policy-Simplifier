import torch
from transformers import AutoTokenizer,AutoModelForSeq2SeqLM
from app.config import MODEL_PATH
import re

PREFIX="summarize privacy policy: "

class PolicySummarizer:

    def  __init__(self):
        self.device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer=None
        self.model=None
        self.load_model()
        
    def load_model(self):
        self.model=AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH).to(self.device)
        self.tokenizer=AutoTokenizer.from_pretrained(MODEL_PATH)
        
        self.model.eval()
        
    def summarize(self,text):
        prompt=PREFIX+text
        inputs=self.tokenizer(
            prompt,
            return_tensors='pt',
            max_length=1024,
            truncation=True
        ).to(self.device)
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=128,
            num_beams=4,
            no_repeat_ngram_size=3,
            early_stopping=True
        )
        
        return self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )
        
        
        