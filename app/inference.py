import torch
from transformers import AutoTokenizer,AutoModelForCausalLM
from app.config import *

SUMMARY_PREFIX="""TASK: POLICY_SUMMARY
Write a concise plain-language summary using only facts stated below.

POLICY:
"""

RISK_PREFIX=f"""TASK: PRIVACY_RISK_EXTRACTION
Return valid JSON with every required category. Use only verbatim evidence from the policy.
Use [] when no evidence exists.
Categories: {', '.join(VALID_KINDS)}

POLICY:
"""  

class PolicySummarizer:

    def  __init__(self):
        self.device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer=AutoTokenizer.from_pretrained(TOKENIZER_PATH,trust_remote_code=True)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token=self.tokenizer.eos_token
            
        self.model=AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,
            torch_dtype=torch.float16,
            trust_remote_code=True
        ).to(self.device)
        
        self.model.eval();
        
    def summarize(self,user_template):
        print("Summarizing............")
        inputs = self.tokenizer.apply_chat_template(
            user_template,
            return_tensors="pt",
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True
        ).to(self.device)
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=SUMMARY_MAX_NEW_TOKENS,
            do_sample=False,
            no_repeat_ngram_size=3,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.pad_token_id
        )
        outputs=outputs[0]
        outputs=outputs[inputs['input_ids'].shape[-1]:]
        print("Summary Generated")
        output_text=self.tokenizer.decode(
            outputs,
            skip_special_tokens=True
        )
        return output_text
    
    def tokenize_policy(self,policy_text):
        encoding=self.tokenizer(
            policy_text,
            add_special_tokens=False,
            return_offsets_mapping=True
        )
        
        return (
            encoding['input_ids'],
            encoding['offset_mapping']
        )
        
    def create_chunks(self,input_ids,offset):
        chunks=[]
        start=0
        while(start<len(input_ids)):
            end=min(start+MAX_INPUT_TOKENS,len(input_ids))
            
            char_start=offset[start][0]
            char_end=offset[end-1][1]
            
            chunks.append({
                "char_start":char_start,
                "char_end":char_end
            })
            
            start+=MAX_INPUT_TOKENS-OVERLAP
            
        return chunks
            
        
    def extract_risk(self,assistant_template):
        
        print("Extracting Risks.............")
        inputs = self.tokenizer.apply_chat_template(
            assistant_template,
            return_tensors="pt",
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True
        ).to(self.device)
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=RISK_MAX_NEW_TOKENS,
            do_sample=False,
            no_repeat_ngram_size=3,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.pad_token_id
        )
        outputs=outputs[0]
        outputs=outputs[inputs['input_ids'].shape[-1]:]
        print("Risks Extracted")
        output_text= self.tokenizer.decode(
            outputs,
            skip_special_tokens=True
        )
        return output_text
        
    def generate_output(self,policy_text):
        input_ids,offset=self.tokenize_policy(policy_text)
        
        chunks=self.create_chunks(input_ids,offset)
        if len(chunks)==0:
            return [],[]
        
        summaries=[]
        risk_statements=[]
        
        for chunk in chunks:
            
            chunk_text=policy_text[chunk["char_start"]:chunk["char_end"]]
            user_template=[{
                "role":"user",
                "content":SUMMARY_PREFIX+chunk_text
            }]
            assistant_template=[{
                "role":"user",
                "content":RISK_PREFIX+chunk_text
            }]
            summary=self.summarize(user_template)
            risk=self.extract_risk(assistant_template)
            
            summaries.append(summary)
            risk_statements.append(risk)
            
        return summaries,risk_statements
        
        
        
