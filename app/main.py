import os
from pathlib import Path
from typing import Literal
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from .core import Store, rank
from .generator import ModelError, generate

ROOT = Path(__file__).resolve().parent.parent


class Question(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    top_k: int = Field(default=3, ge=1, le=10)
    mode: Literal["extractive", "llm"] = "extractive"


def create_app(db_path=None):
    app = FastAPI(title="证据问答 · 实习教学基线", version="0.1.0")
    store = Store(db_path or os.getenv("KB_DB_PATH", str(ROOT / "data/kb.sqlite3")))
    app.state.store = store

    @app.get("/")
    def home():
        return FileResponse(ROOT / "web/index.html")

    @app.get("/health")
    def health():
        return {"status": "ok", "retrieval": "lexical_tfidf", "default_mode": "extractive"}

    @app.post("/documents")
    async def upload(file: UploadFile = File(...)):
        try:
            raw = await file.read(2 * 1024 * 1024 + 1)
            if len(raw) > 2 * 1024 * 1024:
                raise HTTPException(413, "文档上限 2 MiB")
            text = raw.decode("utf-8-sig")
            return store.ingest(file.filename or "", text)
        except (UnicodeDecodeError, ValueError) as exc:
            raise HTTPException(400, "文件编码必须为 UTF-8" if isinstance(exc, UnicodeDecodeError) else str(exc)) from None
        finally:
            await file.close()

    @app.get("/documents")
    def documents():
        return store.documents()

    @app.delete("/documents/{document_id}")
    def delete(document_id: str):
        if not store.delete(document_id):
            raise HTTPException(404, "文档不存在")
        return {"deleted": True}

    @app.post("/query")
    def query(body: Question):
        question = body.question.strip()
        if not question:
            raise HTTPException(422, "问题不能为空")
        hits = rank(question, store.chunks(), body.top_k)
        if not hits:
            answer = "当前资料中没有找到相关证据，无法可靠回答。"
            store.record(question, answer, body.mode)
            return {"answer": answer, "sources": [], "mode": body.mode, "status": "no_evidence", "usage": {}}
        usage = {}
        status = "answered"
        if body.mode == "llm":
            try:
                answer, ids, usage, abstained = generate(question, hits)
            except ModelError as exc:
                raise HTTPException(502, str(exc)) from None
            sources = [] if abstained else [h for h in hits if h["chunk_id"] in ids]
            if abstained:
                status = "no_evidence"
        else:
            answer = "以下为检索原文摘录，请结合来源判断：\n\n" + "\n\n".join(h["text"] for h in hits)
            sources = hits
        store.record(question, answer, body.mode)
        return {"answer": answer, "sources": sources, "mode": body.mode, "status": status, "usage": usage}

    @app.get("/history")
    def history():
        return store.history()

    return app


app = create_app()
