from app.config import *
from app.inference import PolicySummarizer

summarizer=PolicySummarizer()

text="When you purchase a subscription, we collect your billing address, payment details, and transaction history."

summary,risks=summarizer.generate_output(text)
print(summary)
print(risks)