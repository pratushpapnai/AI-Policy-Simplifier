from transformers import pipeline
from app.inference import PolicySummarizer

summarizer = PolicySummarizer()

text='''
When you purchase a subscription, we collect your billing address, payment details, and transaction history. Payment card information is processed securely by third-party payment providers and is not stored on our servers. Transaction records may be retained for up to seven years to comply with tax and financial regulations. We use purchase history to recommend subscription plans and improve customer support.
'''


print("\nSummary\n")
print(summarizer.summarize(text))