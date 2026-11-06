from pathlib import Path
'''任务要求
1. 读取原来的 raw_documents.csv 文件。
2. 使用 Pandas 布尔索引，筛选出 name 缺失的记录。
3. 打印筛选结果。
4. 打印符合条件的记录数量。
提示： 使用刚学过的 .isna() 和 df[条件]，记录数量可以通过 len() 获取。
运行后，应找到：
- id = 3.0
- name = NaN
- 符合条件的记录数量为 1'''

import pandas as pd
project_root = Path(__file__).resolve().parents[2]

# 拼接 CSV 文件路径
csv_path = project_root / "data" / "exercises" / "raw_documents.csv"
print("CSV 路径：", csv_path)
print("文件存在：", csv_path.exists())

# 读取 CSV
df = pd.read_csv(csv_path)
# 布尔索引：筛选 name 列缺失（NaN）的所有记录并打印
print(df[df["name"].isna()])
# 统计 name 缺失的记录数量
print(len(df[df["name"].isna()]))
