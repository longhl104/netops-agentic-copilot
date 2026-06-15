# GitHub Copilot Instructions for NetOps Agentic Co-Pilot

## Project purpose
This repository is a proof-of-concept multi-agent network operations assistant.
It ingests a network log, runs a LangGraph workflow, retrieves troubleshooting context from FAISS, and returns a remediation plan.

## Architecture and flow
- FastAPI backend entrypoint: `main.py`
- LangGraph workflow assembly: `langgraph_workflow.py`
- Agent modules: `agents/`
  - `triage_agent.py`
  - `retrieval_agent.py`
  - `action_reasoning_agent.py`
  - `formatting_agent.py`
- Knowledge base/index builder: `scripts/knowledge_base.py`
- Simple UI client: `streamlit_app.py`
- FAISS index path expected by retrieval agent: `faiss_index/`

Workflow order:
1. triage
2. retrieve
3. reason
4. format

## Coding expectations
- Use Python and keep dependencies minimal.
- Prefer clear, deterministic logic over hidden side effects.
- Preserve public API behavior of `/diagnose` unless explicitly asked to change it.
- Keep `AgentState` fields compatible with current workflow expectations.
- Add type hints for new/modified Python functions when practical.
- Handle errors explicitly with useful messages.
- Avoid logging sensitive values (for example API keys).

## FastAPI and security guidance
- Keep API key authentication in place unless the task explicitly asks to replace it.
- Validate request payloads with Pydantic models.
- Return structured, client-readable error responses.

## Retrieval and knowledge base guidance
- `RetrievalAgent` expects a local FAISS index at `faiss_index`.
- If changing retrieval behavior, preserve compatibility with offline/local development.
- Keep embedding model choices lightweight and reproducible.

## Local development commands
Use a virtual environment in `.venv`.

Typical setup:
- `python -m venv .venv`
- `.venv\Scripts\activate`
- `pip install -r requirements.txt`

Build knowledge base/index:
- `python scripts/knowledge_base.py`

Run API server:
- `python main.py`

Run Streamlit UI:
- `streamlit run streamlit_app.py`

## Scope discipline for Copilot
When generating changes:
- Make focused edits only in files relevant to the task.
- Do not rename files/modules or reorganize folders unless requested.
- Do not introduce large frameworks or cloud services unless requested.
- Keep comments concise and only where code is not self-explanatory.

## Testing and verification
Before finalizing a change (when possible):
- Ensure imports resolve.
- Ensure FastAPI app starts.
- Ensure LangGraph workflow compiles.
- Ensure retrieval path assumptions (`faiss_index`) remain valid.
