# DocuLens 🔍

> Transforming unstructured reports into structured, queryable data — 
> making the messy documents that power critical business decisions usable.

## What is DocuLens?

DocuLens is an open-source document intelligence pipeline that connects 
to real-world document sources, extracts structured information using LLMs, 
and makes that information searchable, queryable, and useful.

Most important documents in companies — regulatory reports, adverse event 
records, filings, contracts — exist as unstructured text. DocuLens changes that.

## Architecture

DocuLens is built in three layers:

| Layer | What it does | Status |
|-------|-------------|--------|
| 1 — Document Explorer | Connect to public APIs, retrieve documents, AI summaries | In Progress |
| 2 — RAG Assistant | Ask natural language questions, get cited answers | Planned |
| 3 — Structured Extraction | Extract validated JSON fields, multi-model evaluation | Planned |

## Connectors

DocuLens is designed to work with multiple document sources:

- FDA MAUDE — Medical device adverse event reports
- Health Canada — Canadian medical device reports  
- SEC EDGAR — Financial filings
- Local PDF / DOCX — Your own documents
- Web - Any public document source

## Quick Start

```bash
git clone https://github.com/TaninEsfandi/document-intelligence-pipeline
cd docuLens
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Project Structure

```text
docuLens/
├── app/
│   ├── connectors/
│   │   └── fda.py
│   ├── transformers/
│   │   └── fda_transformers.py
│   ├── models/
│   │   └── report.py
│   └── main.py
│   └── streamlit_app.py
```

## Tech Stack

Python · FastAPI · LangChain · ChromaDB · 
Azure OpenAI · Pydantic · MLflow · Streamlit

## Status

| 1 — Document Explorer | Connect to public APIs, retrieve documents, AI summaries | Complete |

![DocuLens Dashboard](assets/dashboard.png)