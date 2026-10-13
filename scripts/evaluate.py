"""原创小型诊断集，仅验证教学基线；不是企业效果/泛化性能证明。"""
import json
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from app.core import Store, rank


def main():
    cases = json.loads((ROOT / "data/eval_seed.json").read_text())
    results = []
    with TemporaryDirectory() as folder:
        store = Store(Path(folder) / "kb.db")
        for path in (ROOT / "data/demo").glob("*.md"):
            store.ingest(path.name, path.read_text())
        for case in cases:
            start = time.perf_counter()
            hits = rank(case["question"], store.chunks(), top_k=3)
            expected = case["expected_source"]
            passed = any(h["source"] == expected for h in hits) if expected else not hits
            results.append(dict(case, passed=passed, sources=[h["source"] for h in hits],
                                latency_ms=round((time.perf_counter() - start) * 1000, 3)))
    known = [r for r in results if r["expected_source"]]
    unknown = [r for r in results if not r["expected_source"]]
    report = {"scope": "原创两份教学资料，词法检索，无真实LLM", "cases": results,
              "known_hit_at_3": {"hit": sum(r["passed"] for r in known), "total": len(known)},
              "unknown_rejection": {"correct": sum(r["passed"] for r in unknown), "total": len(unknown)}}
    output = ROOT / "reports/baseline_eval.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
