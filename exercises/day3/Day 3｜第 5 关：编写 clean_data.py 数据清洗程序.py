'''
1. 使用之前学过的方式读取 raw_documents.csv。
2. 使用 for ... in df.iterrows() 遍历全部记录。
3. 通过 pd.isna() 检查 id、name、content 是否缺失。
4. 对非缺失的名称和正文使用 .strip() 去除首尾空格。
5. 使用 name.endswith((".md", ".txt")) 检查文件扩展名。
'''

from pathlib import Path
import pandas as pd
import json

project_root = Path(__file__).resolve().parents[2]
csv_path = project_root / "data" / "exercises" / "raw_documents.csv"
df = pd.read_csv(csv_path)
ids = set()
clean_rows = []
rejected_rows = []
for index, row in df.iterrows():
    missing_mask = row[["id", "name", "content"]].isna().any()

    if missing_mask:
        print(f"第 {index} 行：存在缺失值")
        rejected_rows.append({
            "id": row["id"],
            "name": row["name"],
            "content": row["content"],
            "reason": "missing_value"
        })
        continue
    name = row["name"].strip()
    content = row["content"].strip()
    if not name or not content:
        print(f"第 {index} 行：名称或内容为空")
        rejected_rows.append({
            "id": row["id"],
            "name": row["name"],
            "content": row["content"],
            "reason": "empty_name_or_content"
        })
        continue
    if not name.endswith((".md", ".txt")):
        print(f"第 {index} 行：非法扩展名")
        rejected_rows.append({
            "id": row["id"],
            "name": row["name"],
            "content": row["content"],
            "reason": "illegal_extension"
        })
        continue
    if row["id"] in ids:
        print(f"第 {index} 行：重复 ID")
        rejected_rows.append({
            "id": row["id"],
            "name": row["name"],
            "content": row["content"],
            "reason": "duplicate_id"
        })
        continue
    ids.add(row["id"])
    clean_rows.append({
        "id": row["id"],
        "name": name,
        "content": content
    })
    print(f"第 {index} 行：基础校验通过")
print("有效记录：", len(clean_rows))
print("拒绝记录：", len(rejected_rows))

'''将 clean_rows 转换为 DataFrame。
将 rejected_rows 转换为 DataFrame。
创建项目根目录下的 reports 文件夹。
将两个 DataFrame 分别导出为 clean_documents.csv 和 rejected_rows.csv。
用 pd.read_csv() 重新读取这两个文件，检查记录数和列名。'''
reports_dir = project_root / "reports"
reports_dir.mkdir(parents=True, exist_ok=True)
clean_df = pd.DataFrame(clean_rows)
rejected_df = pd.DataFrame(rejected_rows)
clean_df.to_csv(reports_dir / "clean_documents.csv", index=False)
rejected_df.to_csv(reports_dir / "rejected_rows.csv", index=False)
clean_df = pd.read_csv(reports_dir / "clean_documents.csv")
rejected_df = pd.read_csv(reports_dir / "rejected_rows.csv")
print("clean_documents.csv:", len(clean_df), clean_df.columns)
print("rejected_rows.csv:", len(rejected_df), rejected_df.columns)

'''
1
统计数据总量
统计原始 CSV 文件有多少条记录、清洗后留下多少条、拒绝多少条。
你已经有这些变量：
df、clean_rows、rejected_rows
思考：如何用 len() 得到它们的长度？
2
统计每一种拒绝原因出现的次数
从 rejected_rows 中取出每条记录的 reason，统计各原因的数量。
例如 missing_value 出现了 3 次，就应该得到：
"missing_value": 3
3
生成 JSON 文件
把前两步的统计结果组合成一个字典，再写入 reports/quality_report.json。
最后打开文件，确认内容正确。

目标：
{
  "total_rows": 10,
  "clean_rows": 5,
  "rejected_rows": 5,
  "rejection_reasons": {
    "duplicate_id": 1,
    "missing_value": 3,
    "illegal_extension": 1
  }
}
'''
# 步骤一：统计数据总量。len() 分别取得原始记录数、清洗后保留数、被拒绝数
total = len(df)
cleaned = len(clean_rows)
rejected = len(rejected_rows)

# 步骤二：统计每种拒绝原因出现的次数。用字典累加，key 为原因，value 为计数
reason_counts = {}
for row in rejected_rows:
    reason = row["reason"]
    if reason in reason_counts:
        reason_counts[reason] += 1    # 原因已出现过，计数加一
    else:
        reason_counts[reason] = 1     # 首次出现该原因，初始化为 1

# 步骤三：把统计结果组装成报告字典，结构与题目要求的目标 JSON 一致
quality_report = {
    "total_rows": total,
    "clean_rows": cleaned,
    "rejected_rows": rejected,
    "rejection_reasons": reason_counts
}

# 以写模式打开 quality_report.json，用 json.dump 将字典序列化写入文件
with open(reports_dir / "quality_report.json", "w") as f:
    json.dump(quality_report, f)

# 打印报告，便于在终端快速核对内容是否正确
print(quality_report)

