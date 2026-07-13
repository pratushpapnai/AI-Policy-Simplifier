---
title: Policy Simplifier AI
emoji: 🛡️
colorFrom: orange
colorTo: red
sdk: docker
pinned: false
---

# Policy Simplifier AI

Policy Simplifier AI is a privacy-policy assistant that converts dense policy text into two useful outputs:

1. a plain-language summary, and
2. structured privacy-risk evidence grouped into fixed privacy categories.

The project uses a fine-tuned Qwen model for multitask inference. The production model is based on `Qwen/Qwen2.5-1.5B-Instruct` and is hosted on Hugging Face as:

```text
pratushpapnai/policy_assistant
```

The app is designed as a Dockerized Hugging Face Space with a Streamlit frontend and a FastAPI backend.

## Features

- Paste privacy policies, terms, or policy clauses through a Streamlit UI.
- Generate concise plain-language summaries.
- Extract privacy risks into 20 fixed categories.
- Return supporting evidence clauses for detected risks.
- Process longer policies using token-based chunking.
- Recover useful risk evidence even when the model returns imperfect JSON-like output.
- Deploy using Docker on Hugging Face Spaces.

## Privacy Risk Categories

The backend extracts evidence into these fixed categories:

```text
BasicAccountInfo, ContactInfo, Demographic, GeoInfo, DeviceInfo,
UsageData, InternetHistory, UserGenerated, UserProfileInfo,
CommunicationProv, Payment, Financial, Purchase, HealthFitness,
Biometric, Images, ContentPreferences, Settings, Metadata, Performance
```

## Architecture

```text
User
  │
  ▼
Streamlit frontend
  │  POST /summarize
  ▼
FastAPI backend
  │
  ▼
PolicySummarizer
  │
  ▼
Fine-tuned Qwen model on Hugging Face Hub
```

### Frontend

The frontend is built with Streamlit:

```text
frontend/streamlit_app.py
```

It accepts policy text, sends it to the backend, and displays:

- summary chunks,
- detected risk categories,
- evidence clauses for each category.

### Backend

The backend is built with FastAPI:

```text
backend/api.py
```

It loads `PolicySummarizer` at startup and exposes a `/summarize` endpoint. The backend handles chunking, model inference, risk parsing, and evidence merging.

### Inference

The inference code lives in:

```text
app/inference.py
```

It uses explicit task prompts:

```text
TASK: POLICY_SUMMARY
TASK: PRIVACY_RISK_EXTRACTION
```

The model generates summaries and structured risk outputs separately for each chunk.

## API Contract

### Health Check

```http
GET /
```

Example response:

```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### Summarize and Extract Risks

```http
POST /summarize
```

Request body:

```json
{
  "text": "We collect your billing information, transaction history, and device identifiers..."
}
```

Response body:

```json
{
  "summaries": [
    "The policy says the service collects billing information, transaction history, and device identifiers."
  ],
  "risk_statements": {
    "Payment": ["billing information"],
    "Purchase": ["transaction history"],
    "DeviceInfo": ["device identifiers"]
  }
}
```

The actual `risk_statements` response contains all configured risk categories. Categories with no detected evidence return an empty list.

## Local Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn backend.api:app --reload --port 8000
```

Run the frontend in a second terminal:

```bash
streamlit run frontend/streamlit_app.py
```

Open the Streamlit app in your browser and paste a policy section to analyze it.

## Docker / Hugging Face Spaces

This project is configured for Docker deployment.

Build locally:

```bash
docker build -t policy-simplifier-ai .
```

Run locally:

```bash
docker run -p 7860:7860 policy-simplifier-ai
```

The Docker container uses:

```text
Dockerfile
start.sh
```

`start.sh` starts both:

- FastAPI backend on port `8000`
- Streamlit frontend on port `7860`

Hugging Face Spaces exposes the Streamlit app on port `7860`.

## Project Structure

```text
.
├── app/
│   ├── config.py
│   └── inference.py
├── backend/
│   └── api.py
├── frontend/
│   └── streamlit_app.py
├── training/
│   └── notebooks and training utilities
├── Dockerfile
├── requirements.txt
├── start.sh
└── README.md
```

## Model

Base model:

```text
Qwen/Qwen2.5-1.5B-Instruct
```

Fine-tuned model:

```text
pratushpapnai/policy_assistant
```

The model was trained for a multitask policy-assistant workflow:

- policy summarization,
- privacy-risk evidence extraction.

## Limitations

- The app is not legal advice.
- Output quality depends on the clarity and completeness of the input policy text.
- Long policies are processed in chunks, so summaries may be chunk-level rather than a single global summary.
- The risk extractor expects model output to resemble JSON; the backend includes recovery logic for imperfect JSON-like responses.
- The model may miss evidence or produce incomplete evidence if the policy text is vague, too long, or poorly structured.

## Tech Stack

- Python
- Streamlit
- FastAPI
- Transformers
- PyTorch
- Hugging Face Hub
- Docker

