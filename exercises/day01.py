"""第1天：只修改 TODO 函数。不需要读完整后端。"""
import json
from pathlib import Path


def inspect_document(path):
    # TODO: 用 UTF-8 读取 path，返回如下结构。
    # 提示：Path(path).read_text(encoding="utf-8")、splitlines()、startswith("#")
    raise NotImplementedError("请实现 inspect_document")


if __name__ == "__main__":
    demo = Path(__file__).resolve().parent.parent / "data/demo/policy.md"
    print(json.dumps(inspect_document(demo), ensure_ascii=False, indent=2))
