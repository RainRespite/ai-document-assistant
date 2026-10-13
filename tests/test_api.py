import json
import pytest
import httpx
from fastapi.testclient import TestClient
from app.main import create_app
from app.generator import ModelError, validate_output


@pytest.fixture
def client(tmp_path):
    with TestClient(create_app(tmp_path / "kb.db")) as value:
        yield value


def upload(client, name="policy.md", content="重复导入文档按哈希去重。"):
    return client.post("/documents", files={"file": (name, content.encode(), "text/plain")})


def test_full_workflow(client):
    assert client.get("/health").json()["status"] == "ok"
    doc = upload(client).json()
    assert upload(client).json()["duplicate"]
    answer = client.post("/query", json={"question": "重复导入"}).json()
    assert answer["status"] == "answered"
    assert answer["mode"] == "extractive"
    assert answer["sources"][0]["source"] == "policy.md"
    assert client.get("/history").json()[0]["question"] == "重复导入"
    assert client.delete("/documents/" + doc["document_id"]).status_code == 200
    assert client.get("/documents").json() == []


def test_no_evidence_and_validation(client):
    assert client.post("/query", json={"question": "火星天气"}).json()["sources"] == []
    assert upload(client, content="   ").status_code == 400
    assert upload(client, name="file.pdf").status_code == 400
    assert client.post("/query", json={"question": " ", "top_k": 3}).status_code == 422
    assert client.post("/query", json={"question": "问题", "top_k": 999}).status_code == 422
    assert client.post("/documents", files={"file": ("x.md", b"\xff", "text/plain")}).status_code == 400
    assert upload(client, content="a" * (2 * 1024 * 1024 + 1)).status_code == 413


def test_missing_model_config(client, monkeypatch):
    upload(client)
    for key in ["LLM_API_KEY", "LLM_MODEL", "LLM_BASE_URL"]:
        monkeypatch.delenv(key, raising=False)
    assert client.post("/query", json={"question": "重复导入", "mode": "llm"}).status_code == 502


def test_model_fake_success(client, monkeypatch):
    upload(client)
    def fake(question, hits):
        return "重复正文按哈希去重。", [hits[0]["chunk_id"]], {"total_tokens": 100}, False
    monkeypatch.setattr("app.main.generate", fake)
    answer = client.post("/query", json={"question": "重复导入", "mode": "llm"}).json()
    assert answer["sources"] and answer["usage"]["total_tokens"] == 100
    assert answer["status"] == "answered"


def test_model_structured_refusal(client, monkeypatch):
    upload(client)
    monkeypatch.setenv("LLM_BASE_URL", "https://example.invalid/v1")
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    monkeypatch.setenv("LLM_MODEL", "mock")
    original_post = httpx.Client.post
    def reply(self, url, *args, **kwargs):
        if not str(url).startswith("https://example.invalid/"):
            return original_post(self, url, *args, **kwargs)
        return httpx.Response(200, request=httpx.Request("POST", url), json={
            "choices": [{"message": {"content": json.dumps({
                "answer": "检索资料没有说明这一点，无法可靠回答。",
                "citation_ids": [], "abstained": True})}}],
            "usage": {"total_tokens": 20}})
    monkeypatch.setattr(httpx.Client, "post", reply)
    response = client.post("/query", json={"question": "重复导入", "mode": "llm"})
    assert response.status_code == 200
    answer = response.json()
    assert answer["status"] == "no_evidence"
    assert answer["sources"] == []
    assert answer["usage"] == {"total_tokens": 20}
    assert client.get("/history").json()[0]["answer"] == answer["answer"]


def test_model_failure_not_saved(client, monkeypatch):
    upload(client)
    def fake(*args):
        raise ModelError("模型请求超时，未保存回答")
    monkeypatch.setattr("app.main.generate", fake)
    assert client.post("/query", json={"question": "重复导入", "mode": "llm"}).status_code == 502
    assert client.get("/history").json() == []


def test_invalid_model_citation():
    with pytest.raises(ModelError):
        validate_output('{"answer":"测试","citation_ids":["fake"],"abstained":false}', [{"chunk_id": "real"}])
    with pytest.raises(ModelError):
        validate_output("not json", [{"chunk_id": "real"}])


def test_valid_model_output():
    hits = [{"chunk_id": "real"}]
    assert validate_output('{"answer":"无法回答","citation_ids":[],"abstained":true}', hits) == (
        "无法回答", [], True)
    assert validate_output('{"answer":"有依据回答","citation_ids":["real","real"],"abstained":false}', hits) == (
        "有依据回答", ["real"], False)


@pytest.mark.parametrize("data", [
    {"answer": "无法回答", "citation_ids": ["fake"], "abstained": True},
    {"answer": "无法回答", "citation_ids": ["real"], "abstained": True},
    {"answer": "回答", "citation_ids": [], "abstained": False},
    {"answer": "无法回答", "citation_ids": [], "abstained": "true"},
    {"answer": "无法回答", "citation_ids": [], "abstained": 1},
    {"answer": "无法回答", "citation_ids": [], "abstained": None},
    {"answer": "无法回答", "citation_ids": "", "abstained": True},
    {"answer": "回答", "citation_ids": [1], "abstained": False},
    {"answer": 1, "citation_ids": [], "abstained": True},
    {"answer": "   ", "citation_ids": [], "abstained": True},
    {"answer": "无法回答", "citation_ids": []},
])
def test_invalid_model_refusal_or_types(data):
    with pytest.raises(ModelError):
        validate_output(json.dumps(data), [{"chunk_id": "real"}])


def test_oversized_upload_closes_file(tmp_path):
    import asyncio
    from io import BytesIO
    from starlette.datastructures import UploadFile
    from fastapi import HTTPException
    app = create_app(tmp_path / "kb.db")
    upload_endpoint = next(route.endpoint for route in app.routes
                           if getattr(route, "path", None) == "/documents" and "POST" in route.methods)
    file = UploadFile(BytesIO(b"a" * (2 * 1024 * 1024 + 1)), filename="large.md")
    with pytest.raises(HTTPException) as error:
        asyncio.run(upload_endpoint(file))
    assert error.value.status_code == 413
    assert file.file.closed


def test_transport_timeout_without_secret(monkeypatch):
    from app.generator import generate
    monkeypatch.setenv("LLM_BASE_URL", "https://example.invalid/v1")
    monkeypatch.setenv("LLM_API_KEY", "test-secret-do-not-expose")
    monkeypatch.setenv("LLM_MODEL", "mock")
    def fail(*args, **kwargs):
        raise httpx.ReadTimeout("internal transport")
    monkeypatch.setattr(httpx.Client, "post", fail)
    with pytest.raises(ModelError, match="超时") as error:
        generate("问题", [{"chunk_id": "a", "source": "a.md", "text": "内容"}])
    assert "test-secret" not in str(error.value)
