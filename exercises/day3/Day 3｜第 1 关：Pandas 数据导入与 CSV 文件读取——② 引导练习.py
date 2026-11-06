from pathlib import Path
import pandas as pd
'''1. 什么是 DataFrame？
DataFrame 是 Pandas 中用来表示二维表格的数据结构。
你可以把它理解成 Python 里的 Excel 表格。
例如：
id	name	score
1	张三	90
2	李四	85
3	王五	95
在 Pandas 中，可以使用 DataFrame 保存和处理这些数据。
它有两个重要特点：
- 行（Row）：代表一条记录，例如张三的成绩。
- 列（Column）：代表一种字段，例如姓名或成绩。
以后我们可以使用 Pandas 检查空值、查找重复数据、筛选记录。
2. pd.read_csv() 是什么？
它的作用是：读取 CSV 文件，将数据加载为 DataFrame。
import pandas as pddf = pd.read_csv("data.csv")



逐行解释：
import pandas as pd：导入 Pandas，并起一个简短的别名 pd。
pd.read_csv("data.csv")：读取名为 data.csv 的文件。
df = ...：将读取结果保存在变量 df 中。
注意：这里的 data.csv 是示例文件名。实际运行时，文件必须存在于指定路径。
3. df.head() 是什么？
它的作用是：查看 DataFrame 最前面的几行数据。
print(df.head())



默认显示前 5 行数据。
还可以指定数量：
print(df.head(3))



表示只查看前 3 行。
为什么要用它？
因为真实项目中的 CSV 文件可能有上万行，我们通常不需要一次性打印全部数据，只需要先检查前几行是否读取正确。'''
# 获取实战项目根目录
project_root = Path(__file__).resolve().parents[2]

# 拼接 CSV 文件路径
csv_path = project_root / "data" / "exercises" / "raw_documents.csv"

# 检查文件
print("CSV 路径：", csv_path)
print("文件存在：", csv_path.exists())

# 读取 CSV
df = pd.read_csv(csv_path)

# 查看前 5 行
print(df.head())

print("数据行列数：", df.shape)
print("字段名称：", df.columns.tolist())
print("各列缺失值数量：")
print(df.isna().sum())

result = df[df["id"] == 2]
print(result)
