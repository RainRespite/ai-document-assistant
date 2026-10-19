f = open("sample.md", encoding="utf-8")
content = f.read()
f.close()

lines = content.splitlines()
'''你的任务
在上述代码后面继续编写，实现：
1. 创建变量 count = 0。
2. 使用 for 遍历 lines。
3. 使用 startswith("#") 判断当前行是否为标题。
4. 如果是标题，count 加 1。
5. 最后打印标题数量。
预期输出：标题数量：2'''

count = 0
for line in lines:
    if line.startswith("#"):
        count += 1
print("标题数量：", count)
