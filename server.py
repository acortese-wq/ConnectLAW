"""HTTP-Backend für ConnectLAW (FastAPI).

Stellt den juristischen Fach-Chatbot als Streaming-Endpoint bereit, den das
GitHub-Pages-Frontend (docs/) ansprechen kann.

Start:
    pip install -r requirements-server.txt
    uvicorn server:app --host 0.0.0.0 --port 8000

WICHTIG: Der Anthropic-API-Schlüssel bleibt ausschliesslich hier im Backend
(ANTHROPIC_API_KEY). Er darf NIE ins statische Frontend gelangen.

Sitzungen werden serverseitig im Speicher gehalten (einfacher In-Memory-Store).
Für den produktiven Mehrbenutzerbetrieb durch einen persistenten Store ersetzen.
"""

from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from connectlaw.agent import LegalAgent
from connectlaw.config import Config, KNOWLEDGE_DIR, SYSTEM_PROMPT_PATH
from connectlaw.knowledge import load_knowledge, load_system_prompt

# ---------------------------------------------------------------------- #
# Initialisierung (einmalig)
# ---------------------------------------------------------------------- #
config = Config()
config.validate()

_system_prompt = load_system_prompt(SYSTEM_PROMPT_PATH)
_knowledge_text, KNOWLEDGE_FILES = load_knowledge(KNOWLEDGE_DIR)

# Einfacher In-Memory-Sitzungsspeicher: session_id -> LegalAgent
_sessions: dict[str, LegalAgent] = {}

# Zugelassene CORS-Ursprünge (z.B. die GitHub-Pages-URL). Standard: alle.
_cors_origins = os.environ.get("CONNECTLAW_CORS_ORIGINS", "*").split(",")

app = FastAPI(title="ConnectLAW", version="4.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _cors_origins],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def _get_agent(session_id: str) -> LegalAgent:
    agent = _sessions.get(session_id)
    if agent is None:
        agent = LegalAgent(config, _system_prompt, _knowledge_text)
        _sessions[session_id] = agent
    return agent


# ---------------------------------------------------------------------- #
# Schemas
# ---------------------------------------------------------------------- #
class ChatRequest(BaseModel):
    session_id: str
    message: str


class ResetRequest(BaseModel):
    session_id: str


# ---------------------------------------------------------------------- #
# Endpoints
# ---------------------------------------------------------------------- #
@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "model": config.model,
        "effort": config.effort,
        "web_search": config.web_search,
        "knowledge_files": KNOWLEDGE_FILES,
        "active_sessions": len(_sessions),
    }


@app.post("/chat")
def chat(req: ChatRequest) -> StreamingResponse:
    """Streamt die juristische Analyse als text/plain (Chunked)."""
    agent = _get_agent(req.session_id)

    def generate():
        try:
            for chunk in agent.iter_answer(req.message):
                yield chunk
        except Exception as exc:  # robustes Streaming – Fehler an Client melden
            yield f"\n\n[Backend-Fehler: {exc}]"

    return StreamingResponse(generate(), media_type="text/plain; charset=utf-8")


@app.post("/reset")
def reset(req: ResetRequest) -> dict:
    """Löscht den Verlauf einer Sitzung (System-Prompt & [DOK] bleiben)."""
    agent = _sessions.get(req.session_id)
    if agent is not None:
        agent.reset()
    return {"status": "reset", "session_id": req.session_id}
