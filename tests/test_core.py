from pathlib import Path
import pytest
from app.core import Store, rank, split_text


def test_split_preserves_coverage_and_overlap():
    text = "测试正文" * 400
    chunks = split_text(text, size=120, overlap=20)
    reconstructed = chunks[0]["text"] + "".join(c["text"][20:] for c in chunks[1:])
    assert reconstructed == text
    assert split_text("   ") == []
    with pytest.raises(ValueError):
        split_text(text, size=100, overlap=100)


def test_duplicate_and_atomic_delete(tmp_path):
    store = Store(tmp_path / "kb.db")
    first = store.ingest("../policy.md", "资料导入需要检查重复正文。")
    second = store.ingest("copy.txt", "资料导入需要检查重复正文。")
    assert first["name"] == "policy.md"
    assert second["duplicate"]
    assert len(store.documents()) == 1
    assert store.delete(first["document_id"])
    assert store.chunks() == []
    assert not store.delete(first["document_id"])


def test_rank_returns_real_source_and_no_unknown():
    rows = [{"chunk_id": "a:0", "source": "a.md", "text": "重复导入文档按哈希去重"},
            {"chunk_id": "b:0", "source": "b.md", "text": "接口测试使用 TestClient"}]
    assert rank("重复导入", rows)[0]["source"] == "a.md"
    assert rank("火星银河轨道", rows) == []


def test_ingest_bad_document(tmp_path):
    store = Store(tmp_path / "kb.db")
    with pytest.raises(ValueError):
        store.ingest("x.exe", "内容")
    with pytest.raises(ValueError):
        store.ingest("x.md", "!!!")


def test_original_source_lines_survive_leading_blanks():
    chunks = split_text("\n\n# 标题\n正文\n")
    assert chunks[0]["start_line"] == 3
    assert chunks[0]["end_line"] == 4
