# DocuLens 🔍

> Transforming unstructured reports into structured, queryable data, 
> making the messy documents that power critical business decisions usable.

## What is DocuLens?

DocuLens is an open-source document intelligence pipeline that connects 
to real-world document sources, extracts structured information using LLMs, 
and makes that information searchable, queryable, and useful.

Most important documents in companies, regulatory reports, adverse event 
records, filings, contracts, exist as unstructured text. DocuLens changes that.

## Architecture

DocuLens is built in three layers:

| Layer | What it does | Status |
|-------|-------------|--------|
| 1 — Document Explorer | Connect to public APIs, retrieve documents | ✅ Complete |
| 2 — RAG Assistant | Ask natural language questions, get cited answers | ✅ Complete |
| 3 — Structured Extraction | Extract validated causal chains, two-pass LLM evaluation | ✅ Complete |

## Connectors

DocuLens is designed to work with multiple document sources:

- FDA MAUDE: Medical device adverse event reports
- Health Canada: Canadian medical device reports  
- SEC EDGAR: Financial filings
- Local PDF / DOCX: Your own documents
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
│   ├── report_transformers/
│   │   └── fda_transformers.py
│   ├── models/
│   │   ├── report.py
│   │   ├── extraction.py     
│   │   └── critic.py         
│   ├── rag/
│   │   ├── embedder.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   ├── runner.py
│   │   ├── extractor.py      
│   │   └── evaluator.py      
│   ├── main.py
│   └── streamlit_app.py
├── configs/
│   └── prompts/
│       ├── extraction_prompt.txt  
│       └── critic_prompt.txt      
```

## Tech Stack

Python · FastAPI · ChromaDB · Pydantic · Streamlit · 
sentence-transformers · Ollama · MLflow · llama3.1:8b · two-pass LLM evaluation

## Demo

![DocuLens Dashboard](assets/dashboard.png)
![DocuLens RAG Chat](assets/rag_demo.png)
![DocuLens Structured Extraction](assets/layer3_demo.png)