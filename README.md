# DocuLens 🔍

[![Tests](https://github.com/TaninEsfandi/document-intelligence-pipeline/actions/workflows/tests.yml/badge.svg)](https://github.com/TaninEsfandi/document-intelligence-pipeline/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Docker](https://img.shields.io/badge/docker-compose-2496ED?logo=docker&logoColor=white)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> Transforming unstructured reports into structured, queryable data, 
> making the messy documents that power critical business decisions usable.

## What is DocuLens?

DocuLens is an open-source document intelligence pipeline that connects 
to real-world document sources, extracts structured information using LLMs, 
and makes that information searchable, queryable, and useful.

Most important documents in companies, regulatory reports, adverse event 
records, filings, contracts, exist as unstructured text. DocuLens changes that.

## Architecture

DocuLens is built in four layers:

| Layer | What it does | Status |
|-------|-------------|--------|
| 1 — Document Explorer | Connect to public APIs, retrieve documents | ✅ Complete |
| 2 — RAG Assistant | Ask natural language questions, get cited answers | ✅ Complete |
| 3 — Structured Extraction | Extract validated causal chains, two-pass LLM evaluation | ✅ Complete |
| 4 — Agent | ReAct agent that orchestrates search, retrieval, and extraction tools | ✅ Complete |

For the design decisions behind each layer, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Results

| Metric | Result |
|--------|--------|
| Agent tool selection accuracy | 5/5 |
| Answer groundedness | 5/5 |
| Average agent latency | 21.5s |

Measured on 5 test questions with `app/agent/evaluator.py`. Groundedness is a heuristic check: the answer is longer than 50 characters and doesn't say "unknown".

## Quick Start

**With Docker (recommended):**
```bash
git clone https://github.com/TaninEsfandi/document-intelligence-pipeline.git
cd document-intelligence-pipeline
docker compose up --build
```
Then pull the LLM model (first time only):
```bash
docker compose exec ollama ollama pull llama3.1:8b
```
Open http://localhost:8501

**Without Docker:**

Requires Ollama installed — see [ollama.com](https://ollama.com)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.docker.txt
pip install -e .
cp .env.example .env   # optional: defaults work for a local Ollama
ollama pull llama3.1:8b
```

## Project Structure

```text
document-intelligence-pipeline/
├── app/
│   ├── agent/
│   │   ├── graph.py
│   │   ├── tools.py
│   │   └── evaluator.py
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
│   ├── config.py
│   ├── logger.py
│   ├── main.py
│   ├── mcp_server.py
│   └── streamlit_app.py
├── configs/
│   └── prompts/
│       ├── extraction_prompt.txt
│       └── critic_prompt.txt
├── tests/
│   ├── test_extraction.py
│   └── test_retriever.py
├── .github/
│   └── workflows/
│       └── tests.yml
├── .env.example
├── ARCHITECTURE.md
├── docker-compose.yml
├── Dockerfile
└── requirements.docker.txt
```

## Tech Stack

Python · FastAPI · ChromaDB · Pydantic · Streamlit · 
sentence-transformers · Ollama · llama3.1:8b · LangGraph · MCP server · Docker · pytest · GitHub Actions

## Agentic Workflow

The LangGraph ReAct agent selects among three tools:

- `search_documents` — answers questions using RAG
- `retrieve_report` — retrieves FDA reports by device
- `extract_structured_fields` — extracts and validates causal-chain fields

`extract_structured_fields` runs a two-pass LLM pipeline:

1. **Extraction** — the LLM reads the report narrative and fills a Pydantic schema: root cause, hazardous situation, hazard outcome, corrective action, domain (Human / Built / Natural / None/unclear) and traceability (report-stated / partially inferred / primarily inferred).
2. **Critic** — a second LLM call audits the extraction against the original report, checking for self-validation (repeating the report's own conclusions as verified fact), speculative claims with no support in the text, and hedging used in the wrong places. It returns an overall flag: `clean`, `minor` or `major`.

## MCP Integration

DocuLens exposes its tools as an MCP server, allowing Claude Desktop to use DocuLens directly in conversation. Tested with Claude Desktop.

**Available tools via MCP:**
- `search_documents` — semantic search across FDA MAUDE reports, returning matching excerpts (no LLM call, to avoid timeouts)
- `retrieve_report` — fetch live reports from openFDA by device name
- `extract_structured_fields` — two-pass causal chain extraction with critic evaluation

**To connect DocuLens to Claude Desktop:**

1. Open `~/Library/Application Support/Claude/claude_desktop_config.json` (Claude Desktop → Settings → Developer → Edit Config) and add DocuLens under `mcpServers`, using absolute paths to your virtualenv's Python and to `app/mcp_server.py`:
```json
{
  "mcpServers": {
    "doculens": {
      "command": "/path/to/venv/bin/python3",
      "args": ["/path/to/docuLens/app/mcp_server.py"]
    }
  }
}
```

2. Restart Claude Desktop

3. In a new chat, check that **doculens** is enabled in the tools/connectors menu

Once connected, Claude can search your FDA report database, retrieve live reports, and extract structured causal chains — all from a natural language conversation.

## Connectors

**Implemented**

- FDA MAUDE — Medical-device adverse-event reports

**Planned**

- Health Canada medical-device reports
- SEC EDGAR financial filings
- Local PDF and DOCX files
- Public web documents

## Demo

![DocuLens Dashboard](assets/dashboard.png)
![DocuLens RAG Chat](assets/rag_demo.png)
![DocuLens Structured Extraction](assets/layer3_demo.png)