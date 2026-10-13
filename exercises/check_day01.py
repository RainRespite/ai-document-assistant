"""独立练习检查：它不参与教学基线的 pytest 通过统计。"""
from pathlib import Path
from tempfile import TemporaryDirectory
from day01 import inspect_document

with TemporaryDirectory() as folder:
    path = Path(folder) / "sample.md"
    path.write_text("# 标题\n正文\n## 小节\n内容\n", encoding="utf-8")
    result = inspect_document(path)
    assert result == {"name": "sample.md", "lines": 4, "headings": 2, "characters": 17}, result
    path.write_text("", encoding="utf-8")
    assert inspect_document(path) == {"name": "sample.md", "lines": 0, "headings": 0, "characters": 0}
print("第1天练习检查通过；仍需口头解释和独立变式")
