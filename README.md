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

DocuLens is built in four layers:

| Layer | What it does | Status |
|-------|-------------|--------|
| 1 — Document Explorer | Connect to public APIs, retrieve documents | Complete |
| 2 — RAG Assistant | Ask natural language questions, get cited answers | Complete |
| 3 — Structured Extraction | Extract validated causal chains, two-pass LLM evaluation | Complete |
| 4 — Agent | ReAct agent that orchestrates search, retrieval, and extraction tools | Complete |

## Connectors

**Implemented**

- FDA MAUDE — Medical-device adverse-event reports

**Planned**

- Health Canada medical-device reports
- SEC EDGAR financial filings
- Local PDF and DOCX files
- Public web documents

## Quick Start

```bash
git clone https://github.com/TaninEsfandi/document-intelligence-pipeline.git
cd document-intelligence-pipeline
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Structured extraction and the agent use a local LLM through [Ollama](https://ollama.com). Install Ollama, then pull the model:

```bash
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
│   ├── main.py
│   └── streamlit_app.py
├── configs/
│   └── prompts/
│       ├── extraction_prompt.txt  
│       └── critic_prompt.txt      
```

## Tech Stack

Python · FastAPI · ChromaDB · Pydantic · Streamlit · 
sentence-transformers · Ollama · MLflow · llama3.1:8b · two-pass LLM evaluation · LangGraph · MCP server

## Agentic Workflow

The LangGraph ReAct agent selects among three tools:

- `search_documents` — answers questions using RAG
- `retrieve_report` — retrieves FDA reports by device
- `extract_structured_fields` — extracts and validates causal-chain fields

Evaluation results: 5/5 tool selection accuracy, 5/5 groundedness, 21.5s average latency

## MCP Integration

DocuLens exposes its tools as an MCP server, allowing Claude Desktop to use DocuLens directly in conversation.

**Available tools via MCP:**
- `search_documents` — semantic search across FDA MAUDE reports using RAG
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

## Demo

![DocuLens Dashboard](assets/dashboard.png)
![DocuLens RAG Chat](assets/rag_demo.png)
![DocuLens Structured Extraction](assets/layer3_demo.png)