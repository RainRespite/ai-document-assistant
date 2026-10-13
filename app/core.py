"""可运行的教学基线。中文双字词 TF-IDF 属于词法检索，不是语义 Embedding。"""
import hashlib
import math
import re
import sqlite3
from collections import Counter
from contextlib import contextmanager
from pathlib import Path


def clean_text(text):
    # 保留开头空行，避免引用行号与原文件错位。
    return text.replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "").rstrip()


def split_text(text, size=500, overlap=80):
    if size < 100 or not 0 <= overlap < size:
        raise ValueError("切片参数无效")
    lines = clean_text(text).splitlines(keepends=True)
    text = "".join(lines)
    if not text:
        return []
    result = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        segment = text[start:end]
        body = segment.strip()
        if body:
            first = start + len(segment) - len(segment.lstrip())
            last = end - (len(segment) - len(segment.rstrip()))
            result.append({"text": body, "start_line": text[:first].count("\n") + 1,
                           "end_line": text[:last - 1].count("\n") + 1})
        if end == len(text):
            break
        start = end - overlap
    return result


def tokens(text):
    text = text.lower()
    words = re.findall(r"[a-z0-9_]+", text)
    for run in re.findall(r"[\u4e00-\u9fff]+", text):
        words.extend(run[i:i + 2] for i in range(len(run) - 1))
        if len(run) == 1:
            words.append(run)
    return words


def rank(query, rows, top_k=3):
    """小数据集教学实现：每次重建词法向量；大规模需独立索引。"""
    counts = [Counter(tokens(r["text"])) for r in rows]
    df = Counter(term for count in counts for term in count)
    q = Counter(tokens(query))
    if not q:
        return []
    idf = {t: math.log((len(rows) + 1) / (n + 1)) + 1 for t, n in df.items()}
    def vector(count):
        return {t: (1 + math.log(n)) * idf[t] for t, n in count.items() if t in idf}
    qv = vector(q)
    qnorm = math.sqrt(sum(v * v for v in qv.values()))
    found = []
    for row, count in zip(rows, counts):
        v = vector(count)
        norm = math.sqrt(sum(n * n for n in v.values()))
        score = sum(w * v.get(t, 0) for t, w in qv.items()) / (qnorm * norm) if norm and qnorm else 0
        if score > 0:
            found.append(dict(row, score=round(score, 6)))
    return sorted(found, key=lambda r: (-r["score"], r["chunk_id"]))[:top_k]


class Store:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.executescript("""
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY, name TEXT NOT NULL, content_hash TEXT UNIQUE NOT NULL);
            CREATE TABLE IF NOT EXISTS chunks (
                id TEXT PRIMARY KEY, document_id TEXT REFERENCES documents(id) ON DELETE CASCADE,
                text TEXT NOT NULL, start_line INTEGER NOT NULL, end_line INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY, question TEXT NOT NULL, answer TEXT NOT NULL,
                mode TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
            """)

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        try:
            with db:
                yield db
        finally:
            db.close()

    def ingest(self, name, text):
        name = name.replace("\\", "/").rsplit("/", 1)[-1]
        if not name or Path(name).suffix.lower() not in {".md", ".txt"}:
            raise ValueError("当前只支持 UTF-8 的 Markdown / TXT 文件")
        text = clean_text(text)
        chunks = split_text(text)
        if not chunks or not tokens(text):
            raise ValueError("文档没有可检索正文")
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        doc_id = digest[:24]
        with self.connection() as db:
            previous = db.execute("SELECT id,name FROM documents WHERE content_hash=?", (digest,)).fetchone()
            if previous:
                count = db.execute("SELECT count(*) FROM chunks WHERE document_id=?", (previous["id"],)).fetchone()[0]
                return {"document_id": previous["id"], "name": previous["name"], "chunks": count, "duplicate": True}
            db.execute("INSERT INTO documents VALUES (?,?,?)", (doc_id, name, digest))
            for i, chunk in enumerate(chunks):
                db.execute("INSERT INTO chunks VALUES (?,?,?,?,?)", (
                    f"{doc_id}:{i}", doc_id, chunk["text"], chunk["start_line"], chunk["end_line"]))
        return {"document_id": doc_id, "name": name, "chunks": len(chunks), "duplicate": False}

    def documents(self):
        with self.connection() as db:
            return [dict(r) for r in db.execute("""SELECT d.id,d.name,count(c.id) AS chunks
                FROM documents d LEFT JOIN chunks c ON d.id=c.document_id GROUP BY d.id ORDER BY d.name""")]

    def chunks(self):
        with self.connection() as db:
            return [dict(r) for r in db.execute("""SELECT c.id AS chunk_id,d.name AS source,c.text,
                c.start_line,c.end_line FROM chunks c JOIN documents d ON c.document_id=d.id ORDER BY c.id""")]

    def delete(self, document_id):
        with self.connection() as db:
            return db.execute("DELETE FROM documents WHERE id=?", (document_id,)).rowcount > 0

    def record(self, question, answer, mode):
        with self.connection() as db:
            db.execute("INSERT INTO queries(question,answer,mode) VALUES (?,?,?)", (question, answer, mode))

    def history(self):
        with self.connection() as db:
            return [dict(r) for r in db.execute("SELECT * FROM queries ORDER BY id DESC LIMIT 20")]
