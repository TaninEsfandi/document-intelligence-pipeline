# DocuLens Architecture

## Overview

DocuLens is built in four layers, each adding a capability on top of the previous one.

```text
Raw API → Documents → Vectors → Answers → Structured Data → Agent
```

Each layer is independent: you can run Layer 1 without Layer 4, and Layer 3 without Layer 2.

---

## Layer 1 — Document Explorer

**What it does:** Connects to public document APIs and retrieves raw reports.

**Key files:** `app/connectors/fda.py`, `app/report_transformers/fda_transformers.py`

**Design decisions:**

- **Connector pattern:** each data source gets its own connector module. Adding a new source (Health Canada, SEC EDGAR) means adding one file, not touching existing code.
- **Transformer pattern:** raw API responses are normalized into a common record shape (`report_number`, `date_received`, `device_name`, `event_type`, `text`) before anything downstream sees them. The FastAPI layer validates these records against the `ReportOutput` Pydantic model. The rest of the system doesn't know or care where the data came from.

---

## Layer 2 — RAG Assistant

**What it does:** Embeds documents into a vector store and answers natural language questions with cited sources.

**Key files:** `app/rag/embedder.py`, `app/rag/vector_store.py`, `app/rag/retriever.py`, `app/rag/runner.py`

**Design decisions:**

- **sentence-transformers over OpenAI embeddings:** Free, local, no API key required, no data sent to a third party. `all-MiniLM-L6-v2` produces 384-dimensional vectors, fast enough to run on CPU.
- **ChromaDB over Elasticsearch or pgvector:** Zero infrastructure — no separate server, no Postgres instance. For an open-source project, the barrier to running it locally should be as low as possible. In a production setting, pgvector on an existing Postgres instance would be the natural upgrade.
- **Cited answers:** Every RAG answer returns source report numbers, device names, and event types alongside the answer. Auditability is the point — an answer without a source is not useful in a regulatory context.

---

## Layer 3 — Structured Extraction

**What it does:** Extracts a structured causal chain from an unstructured report narrative using a two-pass LLM pipeline.

**Key files:** `app/rag/extractor.py`, `app/rag/evaluator.py`, `app/models/extraction.py`, `app/models/critic.py`

**Design decisions:**

- **Two-pass architecture (extractor + critic):** A single LLM call that extracts and validates in one pass tends to validate its own output — it cannot objectively audit what it just produced. Separating generation from validation into two independent calls prevents this self-validation bias. The critic sees the original report and the extraction, and checks specifically for speculative claims, escape phrases used incorrectly, and conclusions that repeat the report rather than verify it.
- **Pydantic schema with Literals:** The extraction schema uses `Literal` types for `domain` and `traceability`. This forces the LLM to choose from a fixed set of values and raises a `ValidationError` immediately if it does not. No string matching, no post-processing.
- **Ollama over OpenAI:** Cost (free), privacy (data stays local), and control (deterministic model version). The tradeoff is latency — a local 8B model is slower than a cloud API. Acceptable for a document intelligence tool where throughput matters more than real-time response.

---

## Layer 4 — LangGraph Agent

**What it does:** A ReAct agent that decides which tool to use based on the user's question, then uses it.

**Key files:** `app/agent/graph.py`, `app/agent/tools.py`, `app/agent/evaluator.py`

**Design decisions:**

- **LangGraph over a raw tool-use loop:** LangGraph makes the agent's reasoning steps explicit and inspectable. Each node in the graph is a discrete step, which makes debugging and evaluation straightforward.
- **Three tools with clear separation of concerns:** `search_documents` is for questions, `retrieve_report` is for fetching raw records, and `extract_structured_fields` is for structured analysis. The agent selects the right tool based on query intent — evaluated at 5/5 tool-selection accuracy across test cases.
- **Evaluation reads actual tool calls:** The evaluator reads `tool_calls` directly from the agent's raw messages rather than doing keyword matching on the final answer. This is the correct way to evaluate tool selection — you want to know what the agent actually did, not infer it from what it said.

---

## MCP Server

**What it does:** Exposes the same three tools as an MCP server so AI assistants like Claude Desktop can use DocuLens directly.

**Key file:** `app/mcp_server.py`

**Design decisions:**

- **FastMCP:** Minimal boilerplate. Each tool is a decorated function, same as the LangGraph tools.
- **Logs to stderr, not stdout:** The MCP protocol uses stdout for communication. Any log line written to stdout corrupts the protocol. All logging goes to stderr.
- **search_documents returns raw ChromaDB results:** The MCP version of search skips the Ollama call and returns the retrieved documents directly. This avoids timeout issues when Claude Desktop calls the tool, since Ollama inference can take 20+ seconds on CPU.

---

## Production Features

| Feature | Implementation |
|---------|---------------|
| Environment config | `app/config.py` loads `.env` and exposes settings with defaults |
| Logging | `app/logger.py` writes timestamped logs to stderr from the extractor, retriever and agent |
| Unit tests | `tests/` covers Pydantic schema validation and embedding dimensions |
| CI | GitHub Actions runs all tests on every push and pull request to `main` |
| Containerization | Docker Compose runs Ollama and the app as separate services |
