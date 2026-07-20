# LLM Zoomcamp — Homework 5: Monitoring

A RAG (Retrieval-Augmented Generation) assistant for answering questions from the [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) course lessons, with OpenTelemetry-based monitoring that exports traces to SQLite.

## How it works

1. **Data ingestion** — Course lesson markdown files are fetched from the `DataTalksClub/llm-zoomcamp` repository (commit `8c1834d`) via `gitsource`.
2. **Indexing** — Documents are indexed with `minsearch` for keyword search over the `content` field.
3. **RAG pipeline** — A query triggers a search, builds a prompt from the results, and calls the OpenAI API (`gpt-5.4-mini`) to generate an answer.
4. **Tracing** — Every `search`, `llm`, and `rag` step is wrapped in OpenTelemetry spans that record duration, input/output token counts, and cost. Spans are exported to `traces.db` (SQLite) via a custom `SQLiteSpanExporter`.

## Project structure

| File | Description |
|---|---|
| `starter.py` | Entry point — loads data, builds the index, and creates the traced RAG instance |
| `assistant.py` | Runs the RAG query 4 times and reports min/max input tokens and max variance |
| `rag_helper.py` | Base RAG class with search, prompt building, and LLM call logic |
| `rag_traced.py` | `RAGTraced` subclass that instruments each step with OpenTelemetry spans |
| `sqlspan.py` | Custom `SQLiteSpanExporter` that writes spans to a local SQLite database |
| `traces.db` | SQLite database where trace spans are stored |

## Setup

```bash
uv sync          # install dependencies
cp .env.example .env   # add your OPENAI_API_KEY
```

## Usage

```bash
# Run a single query through the RAG pipeline
uv run starter.py

# Run the token-variance analysis (4 iterations)
uv run assistant.py
```