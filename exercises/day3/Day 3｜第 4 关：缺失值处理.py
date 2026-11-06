'''Day 3｜第 4 关：缺失值处理'''
'''请你自己写代码完成：
1. 找出 id、name、content 中任意字段缺失的行。
2. 打印这些行。
3. 打印缺失记录的数量。
提示： 把刚才的判断结果放进 df[条件] 即可，再用 len() 统计数量。
不用删除任何数据，也不要修改原始 CSV。'''
from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parents[2]
csv_path = project_root / "data" / "exercises" / "raw_documents.csv"
df = pd.read_csv(csv_path)
missing_mask = df[["id","name","content"]].isna().any(axis=1)
print(df[missing_mask])
print("缺失记录数量：", missing_mask.sum())

'''1. 使用 dropna()，排除 id、name、content 任意字段缺失的记录。
2. 打印清洗后的 DataFrame。
3. 打印原始记录数量。
4. 打印清洗后记录数量。
预期结果
原始记录
10
缺失记录
3
剩余记录
7
'''
cleaned_df = df.dropna(subset=["id","name","content"])
print("原始记录数量：", len(df))
print("清洗后记录数量：", len(cleaned_df))

print(df.to_string(index=True))
