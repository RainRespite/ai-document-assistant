'''现在请你独立完成以下任务：
1. 读取项目中的 raw_documents.csv。
2. 使用布尔索引筛选 id == 2 的记录。
3. 将筛选结果保存为 id_2_preview.csv，放在当前 day3 文件夹。
4. 导出时不保留 DataFrame 的行索引。
5. 打印保存路径和导出记录数量。
验收标准： 生成的 CSV 应包含 id、name、content 三列，以及 faq.md、faq_copy.md 两条记录。
注意：这是练习文件，不要覆盖原始的 raw_documents.csv，也暂时不要修改正式的 reports 文件。'''
from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parents[2]
csv_path = project_root / "data" / "exercises" / "raw_documents.csv"

df = pd.read_csv(csv_path)
result = df[df["id"] == 2]
result.to_csv("id_2_preview.csv", index=False)
print("保存路径：", "id_2_preview.csv")
print("导出记录数量：", len(result))

check_df = pd.read_csv("id_2_preview.csv")

print("实际保存位置：", Path("id_2_preview.csv").resolve())
print("导出字段：", check_df.columns.tolist())
print(check_df)

duplicate_mask = df["id"].duplicated(keep="first")

print(df[duplicate_mask])
print("重复 ID 记录数：", duplicate_mask.sum())